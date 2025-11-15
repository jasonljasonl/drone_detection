import json
import redis
from kafka.admin import NewTopic
from rest_framework.response import Response
from pymavlink import mavutil
from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
import os
import django
from base.models import Radar, Vehicle
from geopy.distance import geodesic

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


def kafka_consumer():
    consumer = KafkaConsumer(
        'mavlink_messages',
        'distance_messages',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    for message in consumer:
        print(f'{message.topic}: {message.value}')


def calcul_distance(request):
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    detection_list = []
    try:
        detected = get_all_vehicles()

        if not detected:
            return Response('no detected_vehicles_global')

        for radar in Radar.objects.all():
            radar_position = (radar.latitude, radar.longitude)

            for vehicle in detected.values():
                vehicle_position = (vehicle["latitude"], vehicle["longitude"])
                distance_between = geodesic(radar_position, vehicle_position).meters

                data = f'"{radar.name}" detected the vehicle with system_id: "{vehicle["system_id"]}" at {distance_between:.2f} meters'
                detection_list.append(data)

                if distance_between <= 500:
                    Vehicle.objects.update_or_create(
                        system_id=vehicle["system_id"],
                        defaults={
                            "latitude": vehicle["latitude"],
                            "longitude": vehicle["longitude"],
                            "altitude": vehicle["altitude"]
                        }
                    )

        producer.send('distance_messages', detection_list)
        producer.flush()

        return Response(detection_list)

    except Exception as e:
        print('Error:', e)
        return Response({'error': str(e)})
