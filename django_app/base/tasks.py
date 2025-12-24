import time
import json
import redis
from celery.app import shared_task
from rest_framework.response import Response
from pymavlink import mavutil
from kafka import  KafkaProducer
from .models import Radar, Vehicle
from geopy.distance import geodesic
from datetime import datetime

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

@shared_task
def kafka_producer_task(port='14551'):
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

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

@shared_task
def calcul_distance_task():

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
