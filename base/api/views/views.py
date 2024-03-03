from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from base.models import Room
from ..serializers import RoomSerializer
import requests, re, json

# usando api_view - com funções


# Listar todas as salas
@api_view(["GET", "POST"])
def getRooms(request):

    if request.method == "POST":

        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer = RoomSerializer(Room.objects.all(), many=True)
    return Response({"serializer": serializer.data})


# Pegar determinada sala e poder alterá-la ou deletá-la
@api_view(["GET", "PUT", "DELETE", "PATCH"])
def getRoom(request, roomId):
    room = get_object_or_404(Room.objects.all(), pk=roomId)
    if request.method == "GET":
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        room.delete()
        return Response(
            {"DELETED": True, "BACK_TO_HOME": "http://127.0.0.1:8000/api/"},
            status=status.HTTP_204_NO_CONTENT,
        )
    elif request.method == "PATCH":
        serializer = RoomSerializer(room, data=request.data, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Pegar as salas pelo seu tópico
@api_view(["GET"])
def getRoomsForTopic(request, topicId):
    rooms = Room.objects.filter(topic=topicId)

    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)
