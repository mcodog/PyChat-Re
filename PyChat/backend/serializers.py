from rest_framework import serializers
from .models import Chat, ChatLog, Task

# ChatLog Serializer
class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = ['id', 'chat', 'sender', 'message_content', 'timestamp']

# Chat Serializer
class ChatSerializer(serializers.ModelSerializer):
    logs = ChatLogSerializer(many=True, read_only=True)
    class Meta:
        model = Chat
        fields = ['id', 'title', 'description', 'created_at', 'logs']

# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at']
