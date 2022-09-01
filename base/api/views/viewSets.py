from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from base.models import Room
from ..serializers import RoomSerializer

class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer

    #? Django authentication 
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly,]

    #? Filtrar os dados por query strings com a lib - mais prático, menos personalizável
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', '^description', 'topic__id']

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
