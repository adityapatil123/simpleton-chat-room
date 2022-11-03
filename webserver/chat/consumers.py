import json
import time
import asyncio

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import ChatRoomMessage
from chat.serializers import ChatMessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @sync_to_async
    def save_chat_message(self, message):
        data = {
            'room_name': self.room_name,
            'message': message,
        }
        serializer = ChatMessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

    @sync_to_async
    def get_chat_messages(self):
        chat_messages = ChatRoomMessage.objects.filter(room_name=self.room_name)
        serializer = ChatMessageSerializer(chat_messages, many=True)
        return [m['message'] for m in serializer.data]

    # This function receive messages from WebSocket.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg_type = text_data_json["type"]
        # username = text_data_json["username"]
        if msg_type == "chatbox_message":
            await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "chatbox_message",
                        "message": text_data_json["message"],
                    },
                )
            await self.save_chat_message(text_data_json["message"])


        else:
            chat_messages = await self.get_chat_messages()
            await self.send(json.dumps(
                {
                    "messages": chat_messages,
                    "type": "all_messages"
                }))

    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event["message"]
        # username = event["username"]
        #send message and username of sender to websocket
        await self.send(json.dumps(
                {
                    "message": message,
                    "type": "chat"
                }))

