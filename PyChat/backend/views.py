from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Chat, ChatLog, Task
from .serializers import ChatSerializer, ChatLogSerializer, TaskSerializer
from datetime import datetime
import requests

# Replace with your actual latitude, longitude, and API key
lat = "40.7128"  # Example: New York City latitude
lon = "-74.0060"  # Example: New York City longitude
api_key = "7b786a29cb6901b206b317a87d162262"  # Replace with your OpenWeatherMap API key

# Construct the URL for the API request
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"


# Chat Views
class ChatListCreate(APIView):
    def get(self, request):
        chats = Chat.objects.all()
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatLogListByChat(APIView):
    def get(self, request, chat_id):
        # Filter chat logs by chat_id (foreign key relation)
        chat_logs = ChatLog.objects.filter(chat_id=chat_id)

        # If no chat logs are found, return a 404 error
        if not chat_logs.exists():
            return Response({"detail": "No chat logs found for this chat."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data and return the response
        serializer = ChatLogSerializer(chat_logs, many=True)
        return Response(serializer.data)


class ChatDetail(APIView):
    def get(self, request, pk):
        try:
            chat = Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChatSerializer(chat)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            chat = Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChatSerializer(chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            chat = Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ChatLog Views
class ChatLogListCreate(APIView):
    def get(self, request):
        logs = ChatLog.objects.all()
        serializer = ChatLogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatLogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            saved_log = serializer.save()
            process_message = ""
            if ((request.data.get('message_content')).startswith("add a task")):
                process_message = "Adding Task: " + " " + (request.data.get('message_content')).removeprefix("add a task")
            elif ((request.data.get('message_content')) == "what is the time" or (request.data.get('message_content')) == "give me the time"):
                now = datetime.now()
                formatted_time = now.strftime("%I:%M %p")
                process_message = "It is currently " + " " + formatted_time
            elif ((request.data.get('message_content')) == "what is the weather"):
                response = requests.get(url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Store the result (JSON response) in a variable
                    weather_data = response.json()
                    description = weather_data['weather'][0]['description']
                    print(f"Weather: {weather_data}")
                    description = weather_data['weather'][0]['description']
                    temperature = weather_data['main']['temp']
                    city_name = weather_data['name']

                    # Creating the processed message
                    process_message = f"The Weather in {city_name} is {description}. The temperature is {temperature}K."

                else:
                    print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
            else:
                process_message = "Unkown Command."
            ChatLog.objects.create(
                chat=saved_log.chat,  # Set the same chat instance
                message_content=process_message,
                sender="PyChat"
            )
            return Response({ "message_content": process_message, "sender": "PyChat" }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatLogDetail(APIView):
    def get(self, request, pk):
        try:
            log = ChatLog.objects.get(pk=pk)
        except ChatLog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChatLogSerializer(log)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            log = ChatLog.objects.get(pk=pk)
        except ChatLog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChatLogSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            log = ChatLog.objects.get(pk=pk)
        except ChatLog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Task Views
class TaskListCreate(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
