
from asyncore import read
from pydoc_data.topics import topics
from turtle import update
from unicodedata import name
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from rest_framework.fields import SerializerMethodField
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from base.models import Room, Topic, Message
from django.contrib.auth.models import User


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ('name',)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

# Usando 1 serializer para criar e listar models
#? Main serializer  
class RoomSerializer(ModelSerializer):
    #? serializando os models do relacionamento - nested serializers
    topic = TopicSerializer()
    host = UserSerializer(read_only=True)
    days_since_created = SerializerMethodField()
    class Meta:
        model = Room
        fields = ('name', 'description', 'days_since_created', 'topic', 'host', 'id')

    def create(self, data):
        topic = data['topic']
        try:
            top = Topic.objects.get(**topic)
        except ObjectDoesNotExist:
            top = Topic.objects.create(**topic)
            top.save()
        
        del data['topic']
        
        room = Room.objects.create(**data)    
        room.topic = top

        #? adicionando um host aleatorio
        room.host = User.objects.get(pk=1)

        room.save()
        return room

    def get_days_since_created(self, obj):
        return ('%s days' % (now() - obj.created).days )

    def update(self, instance, validated_data):
        room = super(RoomSerializer, self).update(instance, validated_data)
        try:
            validated_data['topic']
            topic = validated_data['topic']
            try:
                top = Topic.objects.get(**topic)
            except ObjectDoesNotExist:
                top = Topic.objects.create(**topic)
                top.save()

            room.topic = top
            room.save()
            del validated_data['topic']
        except:
            pass

        return room




# Usando 2 serializers, um para listar e um para criar
#? serializer para visualizar os campos do model 
class ReadRoomSerializer(ModelSerializer):
    topic = TopicSerializer(read_only=True)
    host = UserSerializer(read_only=True)
    days_since_created = SerializerMethodField()
    class Meta:
        model = Room
        fields = ('name', 'description', 'days_since_created', 'topic', 'host')

    def get_days_since_created(self, obj):
        return ('%s days' % (now() - obj.created).days )


#serializer para criar, deletar ou atualizar os campos do model
class WriteRoomSerializer(ModelSerializer):
    days_since_created = SerializerMethodField()
    host = SlugRelatedField(slug_field='username', queryset = User.objects.all())
    topic = SlugRelatedField(slug_field='name', queryset = Topic.objects.all())
    class Meta:
        model = Room
        fields = ('name', 'description', 'days_since_created', 'topic', 'host')

    def get_days_since_created(self, obj):
        return ('%s days' % (now() - obj.created).days )