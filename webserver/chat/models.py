from django.db import models
from django.contrib.auth.models import User


class ChatRoomMessage(models.Model):
    room_name = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=180)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)

