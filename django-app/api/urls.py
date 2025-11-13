from django.urls import path
from .views import receiving_messages, add_radar, view_radar_list, calcul_distance

urlpatterns = [
    path('detected-objects/', receiving_messages, name='List of detected objects'),
    path('add-radar/', add_radar, name='Add a radar'),
    path('radars-list/', view_radar_list, name='List of available radars'),
    path('dist/', calcul_distance, name='distance')
]