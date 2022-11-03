from rest_framework import serializers
from .models import ChatRoomMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoomMessage
        fields = ["room_name", "message", "timestamp", "user"]
