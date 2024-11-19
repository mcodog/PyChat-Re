from django.db import models
from django.contrib.auth.models import User

# Enum for sender types
class Sender(models.TextChoices):
    USER = "User"
    PYCHAT = "PyChat"

# Chat model
class Chat(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="") 

    def __str__(self):
        return self.title

# ChatLog model (with foreign key to Chat)
class ChatLog(models.Model):
    chat = models.ForeignKey(Chat, related_name="logs", on_delete=models.CASCADE)
    sender = models.CharField(max_length=10, choices=Sender.choices, default=Sender.PYCHAT)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # timestamp when message is created

    def __str__(self):
        return f"Message by {self.sender} in {self.chat.title}"

# Task model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Completed", "Completed")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp when task is created
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="") 

    def __str__(self):
        return self.title
