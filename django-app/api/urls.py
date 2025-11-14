from django.urls import path
from .views import  add_radar, view_radar_list, calcul_distance_view, create_topic_view, \
    run_kafka_producer_view

urlpatterns = [
#   path('detected-objects/', receiving_messages, name='List of detected objects'),
    path('add-radar/', add_radar, name='Add a radar'),
    path('radars-list/', view_radar_list, name='List of available radars'),
    path('dist/', calcul_distance_view, name='distance'),
    path('create-topic/', create_topic_view),
    path('run-producer/', run_kafka_producer_view, name='run_kafka_producer'),

]