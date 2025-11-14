import json
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


connections = {}
detected_vehicles_global = {}


def create_kafka_topic(topic_name='mavlink_messages', bootstrap_servers='localhost:9092'):
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        topic_list = [NewTopic(name=topic_name, num_partitions=1, replication_factor=1)]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print(f'Topic {topic_name} created')
    except Exception as e:
        print(f'Error: {e}')


def kafka_producer(request):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
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
                    "system_id": connection.target_system,
                    "latitude": latitude,
                    "longitude": longitude,
                    "altitude": altitude
                }
                detected_vehicles_global[sysid] = vehicle_data

                producer.send('mavlink_messages', json.dumps(vehicle_data).encode('utf-8') )
                producer.flush()

        except Exception as e:
            print('Error :', e)
            return Response({"error": str(e)})


def kafka_consumer():
    consumer = KafkaConsumer('mavlink_messages', bootstrap_servers=['localhost:9092'], value_deserializer=lambda v: json.loads(v.decode('utf-8')))
    for message in consumer:
        print(f'{message.topic}: {message.value}')


def calcul_distance():
    detection_list = []

    for radar in Radar.objects.all():
        radar_position = (radar.latitude, radar.longitude)

        for vehicle in detected_vehicles_global.values():
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
    return detection_list