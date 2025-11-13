from django.db import models

class Vehicle(models.Model):
    system_id = models.IntegerField()
    latitude = models.FloatField(max_length=256)
    longitude = models.FloatField(max_length=256)
    altitude = models.FloatField(max_length=256)
    detected_timestamp = models.DateTimeField(auto_now_add=True)


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
    radar_range = models.CharField(max_length=30)
    status_type = {'active':'active',
                   'inactive':'inactive',
                   'paused':'paused'
                   }
    status = models.CharField(choices=radar_type)
    installation_date = models.DateTimeField(auto_now_add=True)


class Detection(models.Model):
    event_timestamp = models.DateTimeField(auto_now_add=True)
    event_position = models.CharField(max_length=256)
    event_log = models.TextField()
    radar = models.ForeignKey(Radar, on_delete=models.CASCADE)
