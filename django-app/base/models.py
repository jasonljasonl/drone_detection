from django.db import models
from django.db.models import ForeignKey



class Radar(models.Model):
    name = models.CharField(max_length=256)
    radar_type = {'RF_sensor':'RF_sensor',
                  'DF_sensor':'DF_sensor',
                  'camera':'camera',
                  'remote_id-sensor': 'remote_id-sensor',
                  'radar':'radar'
                  }
    type = models.CharField(choices=radar_type)
    latitude = models.FloatField(max_length=256, default=0)
    longitude = models.FloatField(max_length=256, default=0)
    altitude = models.FloatField(max_length=256,  default=0)
    radar_range = models.FloatField(max_length=30)
    status_type = {'active':'active',
                   'inactive':'inactive',
                   'paused':'paused'
                   }
    status = models.CharField(choices=status_type)
    installation_date = models.DateTimeField(auto_now_add=True)


class Vehicle(models.Model):
    system_id = models.IntegerField()
    latitude = models.FloatField(max_length=256)
    longitude = models.FloatField(max_length=256)
    altitude = models.FloatField(max_length=256)
    detected_timestamp = models.DateTimeField(auto_now_add=True)
    detected_radar = models.ForeignKey(Radar, on_delete=models.CASCADE, default=None)


class EventDetectionLog(models.Model):
    log_creation_date = models.DateTimeField(auto_now_add=True)
    related_vehicle = ForeignKey(Vehicle, on_delete=models.CASCADE)
    radar = models.ForeignKey(Radar, on_delete=models.CASCADE)
