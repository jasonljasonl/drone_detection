import time
import json
import redis
from kafka.admin import NewTopic
from rest_framework.response import Response
from pymavlink import mavutil
from kafka import  KafkaProducer, KafkaAdminClient
import os
import django
from base.models import Radar, Vehicle
from geopy.distance import geodesic
from channels.layers import get_channel_layer
from aiokafka import AIOKafkaConsumer
import logging
from datetime import datetime

timestamp = datetime.now().isoformat()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dvrc.settings")
django.setup()

r = redis.Redis(host='localhost', port=6379, db=0)

connections = {}


def save_vehicle(vehicle):
    vehicle_id = vehicle["system_id"]
    vehicle_json = json.dumps(vehicle)
    r.hset("detected_vehicles", vehicle_id, vehicle_json)


def get_all_vehicles():
    result = {}
    data = r.hgetall("detected_vehicles")
    for key,value in data.items():
        vehicle_id = int(key)
        vehicle_data = json.loads(value)
        result[vehicle_id] = vehicle_data
    return result


def create_kafka_topic(bootstrap_servers='localhost:9092'):
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        topic_list = [
            NewTopic(name='mavlink_messages', num_partitions=1, replication_factor=1),
            NewTopic(name='distance_messages', num_partitions=1, replication_factor=1)
        ]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print('Topics created')
    except Exception as e:
        print(f'Error: {e}')


def kafka_producer(request):
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    port = request.GET.get('port', '14551')
    if port not in connections:
        connections[port] = mavutil.mavlink_connection(f'udpin:0.0.0.0:{port}')
        connections[port].wait_heartbeat()
    connection = connections[port]
    print('Connected to mavlink, sending messages...')
    while True:
        try:
            message = connection.recv_match(type='GPS_RAW_INT', blocking=True)
            if message:
                sysid = connection.target_system
                latitude = message.lat / 1e7
                longitude = message.lon / 1e7
                altitude = message.alt / 1000

                vehicle_data = {
                    "system_id": sysid,
                    "latitude": latitude,
                    "longitude": longitude,
                    "altitude": altitude
                }

                save_vehicle(vehicle_data)

                producer.send('mavlink_messages', vehicle_data)
                producer.flush()

        except Exception as e:
            print('Error :', e)
            return Response({'error': str(e)})


async def kafka_consumer():
    consumer = AIOKafkaConsumer(
        'mavlink_messages',
        'distance_messages',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    await consumer.start()

    channel_layer = get_channel_layer()
    try:
        async for message in consumer:
            print(f'{message.topic}: {message.value}')
            await channel_layer.group_send (
                'mavlink_group',
                {
                    'type':'mavlink_message',
                    'topic': message.topic,
                    'data': message.value
                }
            )
    finally:
        await consumer.stop()


logger = logging.getLogger('myapp')
logger.setLevel(logging.WARNING)

if not logger.handlers:
    handler = logging.FileHandler('kafka_log.log', encoding='utf-8')
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)



def calcul_distance(request):

    is_vehicle_in_zone_state = {}

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    try:
        radars = list(Radar.objects.all())

        while True:
            detection_list = []

            detected = get_all_vehicles()
            if not detected:
                continue

            for radar in radars:
                radar_position = (radar.latitude, radar.longitude)

                for vehicle in detected.values():
                    system_id = vehicle["system_id"]
                    vehicle_position = (vehicle["latitude"], vehicle["longitude"])
                    distance_between = geodesic(radar_position, vehicle_position).meters

                    vehicle_in_zone = distance_between <= 500
                    vehicle_was_in_zone = is_vehicle_in_zone_state.get(system_id, False)

                    if vehicle_in_zone and not vehicle_was_in_zone:
                        timestamp = datetime.now().isoformat()
                        logger.warning(
                            f'Vehicle with ID : {system_id} has been detected by radar: {radar.name} '
                            f'at latitude: {vehicle["latitude"]}, longitude: {vehicle["longitude"]} '
                            f'and altitude {vehicle["altitude"]} at {timestamp}'
                        )

                    is_vehicle_in_zone_state[system_id] = vehicle_in_zone

                    data = {
                        "radar": radar.name,
                        "system_id": system_id,
                        "distance": distance_between,
                        "radar_position": radar_position
                    }
                    producer.send('distance_messages', data)

                    detection_list.append(data)

                    if vehicle_in_zone:
                        vehicle_obj, created = Vehicle.objects.get_or_create(
                            system_id=system_id,
                            defaults={
                                "latitude": vehicle["latitude"],
                                "longitude": vehicle["longitude"],
                                "altitude": vehicle["altitude"],
                                "detected_radar": radar
                            }
                        )
                        if not created:
                            vehicle_obj.latitude = vehicle["latitude"]
                            vehicle_obj.longitude = vehicle["longitude"]
                            vehicle_obj.altitude = vehicle["altitude"]
                            vehicle_obj.save()


            for detection in detection_list:
                producer.send('distance_messages', detection)
            producer.flush()
            time.sleep(1)

    except Exception as e:
        print('Error:', e)
        return Response({'error': str(e)})
