from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Chat, ChatLog, Task
from .serializers import ChatSerializer, ChatLogSerializer, TaskSerializer
from datetime import datetime
import requests
from g4f.client import Client
import g4f
import webbrowser

client = Client()
def chatwithgpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        provider=g4f.Provider.openai,
        messages=[{"role": "user", "content": prompt}],
        # Add any other necessary parameters
    )
    return response.choices[0].message.content


import spacy
from spacy.matcher import Matcher
import requests
from datetime import datetime
import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyAxeHL1Udglxp68hrMh37rWlyq9_NWp3eg')

model = genai.GenerativeModel("gemini-1.5-flash")

# Load SpaCy's English model
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

# Define patterns for various intents
matcher.add("ADD_TASK", [[{"LOWER": "add"}, {"LOWER": "a"}, {"LOWER": "task"}]])
matcher.add("GET_TIME", [[{"LOWER": "what"}, {"LOWER": "is"}, {"LOWER": "the"}, {"LOWER": "time"}],
                         [{"LOWER": "give"}, {"LOWER": "me"}, {"LOWER": "the"}, {"LOWER": "time"}],
                         [{"LOWER": "what"}, {"LOWER": "time"}, {"LOWER": "is"}, {"LOWER": "it"}]],)
matcher.add("OPEN_CHROME", [[{"LOWER": "open"}, {"LOWER": "chrome"}],],)
matcher.add("OPEN_YOUTUBE", [[{"LOWER": "open"}, {"LOWER": "youtube"}],],)
matcher.add("GET_WEATHER", [[{"LOWER": "what"}, {"LOWER": "is"}, {"LOWER": "the"}, {"LOWER": "weather"}],
                            [{"LOWER": "tell"}, {"LOWER": "me"}, {"LOWER": "the"}, {"LOWER": "weather"}],
                            [{"LOWER": "weather"}, {"LOWER": "now"}]])

def get_lat_lon(city_name, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude
        else:
            return "City not found", None
    else:
        return f"Error: {response.status_code}", None

def extract_city_name(message_content):
    doc = nlp(message_content)
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Look for geopolitical entities
            return ent.text
    return None  # No city found

from rest_framework import serializers

# Replace with your actual latitude, longitude, and API key


# Construct the URL for the API request



# Chat Views
class ChatListCreate(APIView):
    def get(self, request):
        chats = Chat.objects.prefetch_related('logs').all().order_by('-id')  # Prefetch `logs` to optimize queries
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
            saved_log = serializer.save()  # Save the first ChatLog

            if request.data.get('sender') == 'PyChat':
                return Response({"message_content": request.data.get('message_content'), "sender": "PyChat"}, status=status.HTTP_201_CREATED)

            # Ensure that the 'chat' field is assigned correctly
            if not saved_log.chat:
                return Response({"error": "Chat is not assigned to the log."}, status=status.HTTP_400_BAD_REQUEST)

            process_message = ""
            message_content = request.data.get('message_content')

            doc = nlp(message_content)
            matches = matcher(doc)

            if not matches:
                # generateAi = model.generate_content(message_content)
                # print(generateAi)
                # process_message = generateAi.text
                process_message = chatwithgpt(message_content)
            else:
                # Identify the first match
                match_id = matches[0][0]
                match_name = nlp.vocab.strings[match_id]

                if match_name == "ADD_TASK":
                    process_message = "Adding Task: " + message_content.removeprefix("add a task")
                elif match_name == "GET_TIME":
                    print("Error Here")
                    now = datetime.now()
                    formatted_time = now.strftime("%I:%M %p")
                    process_message = f"It is currently {formatted_time}"
                # elif message_content == "what is the weather":
                #     api_key = "7b786a29cb6901b206b317a87d162262"
                #     city = "London"
                #     lat, lon = get_lat_lon(city, API_KEY)
                #     url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
                #     response = requests.get(url)
                #     if response.status_code == 200:
                #         weather_data = response.json()
                #         description = weather_data['weather'][0]['description']
                #         temperature = weather_data['main']['temp']
                #         city_name = weather_data['name']
                #         process_message = f"The weather in {city_name} is {description}. The temperature is {temperature}K."
                elif match_name == "GET_WEATHER":
                    city_name = extract_city_name(message_content)
                    if city_name:
                        api_key = "7b786a29cb6901b206b317a87d162262"  # Replace with your OpenWeatherMap API key
                        lat, lon = get_lat_lon(city_name, api_key)
                        if lat and lon:
                            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
                            response = requests.get(url)
                            if response.status_code == 200:
                                weather_data = response.json()
                                description = weather_data['weather'][0]['description']
                                temperature = weather_data['main']['temp']
                                process_message = f"The weather in {city_name} is {description}. The temperature is {temperature}K."
                            else:
                                process_message = "Error: Unable to fetch weather data."
                        else:
                            process_message = f"Could not determine latitude and longitude for {city_name}."
                    else:
                        process_message = "Please specify a city name to check the weather."
                elif match_name == "OPEN_CHROME":
                    process_message = "Opening Chrome..."
                    webbrowser.open('https://www.google.com')
                elif match_name == "OPEN_YOUTUBE":
                    process_message = "Opening YouTube..."
                    webbrowser.open('https://www.youtube.com')


            # Create a new ChatLog instance with the same chat (saved_log.chat)
            new_chat_log = ChatLog.objects.create(
                chat=saved_log.chat,  # Use the same chat instance
                message_content=process_message,
                sender="PyChat"
            )

            return Response({"message_content": process_message, "sender": "PyChat"}, status=status.HTTP_201_CREATED)

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
