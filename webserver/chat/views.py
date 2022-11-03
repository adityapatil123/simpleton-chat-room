from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import ChatRoomMessage
from .serializers import ChatMessageSerializer


def home(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


class ChatMessageListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = []

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = ChatRoomMessage.objects.filter(user=request.user.id)
        serializer = ChatMessageSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'room_name': request.data.get('room_name'),
            'message': request.data.get('message'),
            'user': request.user.id
        }
        serializer = ChatMessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatMessageDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, chat_message_id, user_id):
        '''
        Helper method to get the object with given chat_message_id, and user_id
        '''
        try:
            return ChatRoomMessage.objects.get(id=chat_message_id, user = user_id)
        except ChatRoomMessage.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, chat_message_id, *args, **kwargs):
        '''
        Retrieves the Todo with given chat_message_id
        '''
        todo_instance = self.get_object(chat_message_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ChatMessageSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, chat_message_id, *args, **kwargs):
        '''
        Updates the todo item with given chat_message_id if exists
        '''
        chat_message_instance = self.get_object(chat_message_id, request.user.id)
        if not chat_message_instance:
            return Response(
                {"res": "Object with chat message id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'message': request.data.get('message'),
        }
        serializer = ChatMessageSerializer(instance = chat_message_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, chat_message_id, *args, **kwargs):
        '''
        Deletes the todo item with given chat_message_id if exists
        '''
        todo_instance = self.get_object(chat_message_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
