from django.urls import path
from . import views

urlpatterns = [
    # Chat endpoints
    path('chats/', views.ChatListCreate.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', views.ChatDetail.as_view(), name='chat-detail'),

    path('chat_logs/messages/<int:chat_id>/', views.ChatLogListByChat.as_view(), name='chat-log-list-by-chat'),

    # ChatLog endpoints
    path('chat_logs/', views.ChatLogListCreate.as_view(), name='chat-log-list-create'),
    path('chat_logs/<int:pk>/', views.ChatLogDetail.as_view(), name='chat-log-detail'),

    # Task endpoints
    path('tasks/', views.TaskListCreate.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='task-detail'),
]