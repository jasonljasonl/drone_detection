from django.urls import path
from .views import add_radar, view_radar_list, create_topic_view, \
    realtime_view, view_radar_by_id

urlpatterns = [
    path('add-radar/', add_radar, name='Add a radar'),
    path('radars-list/', view_radar_list, name='List of available radars'),
    path('radar/<int:id>/', view_radar_by_id, name='View radar by ID'),
    path('create-topic/', create_topic_view),
    path('live/', realtime_view, name='data'),
]