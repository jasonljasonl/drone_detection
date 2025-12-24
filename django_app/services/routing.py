from django.urls import re_path
from services.consumer import MavlinkChannelConsumer

websocket_urlpatterns = [
    re_path(r'ws/mavlink/$', MavlinkChannelConsumer.as_asgi()),
]