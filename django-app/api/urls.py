from django.urls import path
from .views import receiving_messages

urlpatterns = [
    path('listen/', receiving_messages, name='receiving_messages'),
]