from dataclasses import field
from email import message
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from django.utils.timezone import now
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

class RoomSerializer(ModelSerializer):
    #? serializando os models do relacionamento - nested serializers
    topic = TopicSerializer()
    host = UserSerializer()
    days_since_created = SerializerMethodField()
    class Meta:
        model = Room
        fields = ('name', 'description', 'days_since_created', 'topic', 'host')
       
    def get_days_since_created(self, obj):
        return ('%s days' % (now() - obj.created).days )