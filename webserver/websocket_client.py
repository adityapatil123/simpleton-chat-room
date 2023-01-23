# import json
#
# from websocket import create_connection
#
# ws = create_connection("ws://localhost:8000/ws/chat/2/")
# print("Sending 'Hello, World'...")
# ws.send(json.dumps({"type": "chatbox_message", "message": "Hello, World"}))
# ws.close()
import json
import os
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def event_triger():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat_new4',
        {
            'type': 'chatbox_message',
            'message': "from script"
        }
    )

print(event_triger())
