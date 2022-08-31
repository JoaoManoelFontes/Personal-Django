from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from base.models import Room
from .serializers import RoomSerializer
import requests, re, json

#usando api_view - com funções

# Listar todas as salas
@api_view(['GET','POST'])
def getRooms(request):

    if request.method == 'POST':

        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    serializer = RoomSerializer(Room.objects.all(), many=True)
    return Response({"serializer":serializer.data})


# Pegar determinada sala e poder alterá-la ou deletá-la
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def getRoom(request, roomId):
    room = get_object_or_404(Room.objects.all(), pk=roomId)
    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data, status = status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = RoomSerializer(room, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
            
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        room.delete()
        return Response({'DELETED':True, 'BACK_TO_HOME':'http://127.0.0.1:8000/api/'}, status = status.HTTP_204_NO_CONTENT)
    elif request.method == 'PATCH':
        serializer = RoomSerializer(room, data=request.data, partial=True)
        return Response(serializer.data, status = status.HTTP_200_OK)


# Pegar as salas pelo seu tópico
@api_view(['GET'])
def getRoomsForTopic(request, topicId):
        rooms = Room.objects.filter(topic = topicId)
        
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

# consumir a api das licitações
def get_data_from_api():    
    request = json.loads(requests.get("http://nadic.ifrn.edu.br/api/dou/2022-02-08/?usuario=dev_nadic").content).get('licitacoes')

    return request[0]

# Usando ModelViewSet - com classes
class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer

    #? Filtrar os dados por query strings com a lib - mais prático, menos personalizável
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    # definir o model que será retornado
    def get_queryset(self):

        #? Filtrar os dados por query strings - Da pra personalizar
        id=self.request.query_params.get("id", None)
        room = Room.objects.filter(pk=id)
        if room:
            return room
        return Room.objects.all()

    # Sobreescrendo as actions do CRUD

    # def list(self, request):
    #     return Response(self.serializer_class(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)  
    
    def create(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        room = Room.objects.all().get(pk=kwargs['pk'])
        serializer = self.serializer_class(room)
        return Response({"serializer":serializer.data})

    def retrieve(self, request, *args, **kwargs):
        room = Room.objects.all().get(pk=kwargs['pk'])
        serializer = self.serializer_class(room)
        return Response({"serializer":serializer.data})

    def update(self, request, *args, **kwargs):
        room = Room.objects.all().get(pk=kwargs['pk'])
        serializer = self.serializer_class(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"serializer":serializer.data})
        else:
            return Response({"error": serializer.errors})
     
    def partial_update(self, request, *args, **kwargs):
        room = Room.objects.all().get(pk=kwargs['pk'])
        serializer = self.serializer_class(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"serializer":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # Criar uma própria action - pegar as salas pelo tópico
    @action(methods=['get'], detail=True)
    def topics(self, request, pk=None):
        rooms = Room.objects.filter(topic = pk)
        if not rooms:
            return Response({"Error":"There is not a room with this topic!"}, status=status.HTTP_400_BAD_REQUEST) 
        serializer = self.serializer_class(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
