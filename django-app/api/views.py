from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RadarSerializer
from base.models import Radar, Vehicle
from services.kafka_services import create_kafka_topic, kafka_producer, calcul_distance

connections = {}
detected_vehicles_global = {}


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


@api_view(['POST'])
def create_topic_view(request):
    topic_name = request.data.get('topic')
    kafka_topic = create_kafka_topic(topic_name)
    return Response({'result': kafka_topic})


@api_view(['GET','POST'])
def run_kafka_producer_view(request):
    return kafka_producer(request)


@api_view(['GET'])
def calcul_distance_view(request):
    return calcul_distance(request)

def realtime_view(request):
    return render(request, 'services/tr.html')