from rest_framework import serializers
from .models import Chat, ChatLog, Task

# Chat Serializer
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'title', 'description', 'created_at']

# ChatLog Serializer
class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = ['id', 'chat', 'sender', 'message_content', 'timestamp']

# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at']
