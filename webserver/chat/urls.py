from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:room_name>/', views.room, name='room'),
    path('api', views.ChatMessageListApiView.as_view()),
    path('api/<int:chat_message_id>/', views.ChatMessageDetailApiView.as_view()),
]