from rest_framework import serializers
from .models import Chat, ChatLog, Task
from django.contrib.auth.models import User

# ChatLog Serializer
class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = ['id', 'chat', 'sender', 'message_content', 'timestamp']

# Chat Serializer
class ChatSerializer(serializers.ModelSerializer):
    logs = ChatLogSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) # This will display the user's string representation (e.g., username)
    
    class Meta:
        model = Chat
        fields = ['id', 'title', 'description', 'created_at', 'logs', 'user']

# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at', 'user']
