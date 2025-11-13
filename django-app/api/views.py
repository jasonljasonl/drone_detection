from platform import system

from rest_framework.response import Response
from rest_framework.decorators import api_view
from pymavlink import mavutil
from .serializers import RadarSerializer
from base.models import Radar, Vehicle
from geopy.distance import geodesic

connections = {}
detected_vehicles_global = {}

@api_view(['GET'])
def receiving_messages(request):

    port = request.GET.get('port', '14551')
    try:
        if port not in connections:
            connections[port] = mavutil.mavlink_connection(f'udpin:0.0.0.0:{port}')
            connections[port].wait_heartbeat()
        connection = connections[port]
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
        else:
            vehicle_data = {"error":"no message"}

        return Response(vehicle_data)

    except Exception as e:
        print('Error :', e)
        return Response({"error": str(e)})


@api_view(['POST'])
def add_radar(request):
    serializer = RadarSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def view_radar_list(request):
    radars = Radar.objects.all()
    serializer = RadarSerializer(radars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def calcul_distance(request):
    detection_list = []

    for radar in Radar.objects.all():
        radar_position = (radar.latitude, radar.longitude)

        for vehicle in detected_vehicles_global.values():
            vehicle_position = (vehicle["latitude"], vehicle["longitude"])
            distance_between = geodesic(radar_position, vehicle_position).meters

            data = f'{radar.name} detected the vehicle with system_id: {vehicle["system_id"]} at {distance_between:.2f} meters'
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

    return Response(detection_list)

