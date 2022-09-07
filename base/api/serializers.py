
from rest_framework.serializers import ModelSerializer, SlugRelatedField
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
    # topic = TopicSerializer()
    # host = UserSerializer()
    host = SlugRelatedField(slug_field='username', queryset = User.objects.all())
    topic = SlugRelatedField(slug_field='name', queryset = Topic.objects.all())
    class Meta:
        model = Room
        fields = ('name', 'description', 'topic', 'host')



#serializer para visualizar os campos do model 
class ReadRoomSerializer(ModelSerializer):
    #? serializando os models do relacionamento - nested serializers
    topic = TopicSerializer()
    host = UserSerializer()
    days_since_created = SerializerMethodField()
    class Meta:
        model = Room
        fields = ('name', 'description', 'days_since_created', 'topic', 'host')
       
    def get_days_since_created(self, obj):
        return ('%s days' % (now() - obj.created).days )


#serializer para criar, deletar ou atualizar os campos do model
class WriteRoomSerializer(ModelSerializer):
    #? serializando os models do relacionamento - nested serializers
    # topic = TopicSerializer()
    # host = UserSerializer()
    host = SlugRelatedField(slug_field='username', queryset = User.objects.all())
    topic = SlugRelatedField(slug_field='name', queryset = Topic.objects.all())
    class Meta:
        model = Room
        fields = ('name', 'description', 'topic', 'host')