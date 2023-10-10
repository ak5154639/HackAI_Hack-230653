from django.db import models
from django.contrib.auth.models import User

class tempData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    lower_temperature = models.FloatField(default=0)
    upper_temperature = models.FloatField(default=100)
    city = models.TextField(default="Delhi")

class alertTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_to_send_alert")
    sent = models.BooleanField(default=False)