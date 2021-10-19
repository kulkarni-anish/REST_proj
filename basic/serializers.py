
from rest_framework import serializers
from .models import MyUser, Notes, ToDo, Workspace
from django.utils import timezone



# class Todoserializer(serializers.Serializer):
#     name        = serializers.CharField(max_length=50)
#     description = serializers.CharField(max_length=500)
#     status      = serializers.BooleanField(default=False)
#     date        = serializers.DateTimeField()
#     updates     = serializers.IntegerField(default=0)
#     deadline    = serializers.DateTimeField(default=timezone.now)

#     def create(self, validated_data):
#         return ToDo.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name  = validated_data.get('name', instance.name)
#         instance.description  = validated_data.get('description', instance.description)
#         instance.status  = validated_data.get('status', instance.status)
#         instance.date  = validated_data.get('date', instance.date)
#         instance.updates  = validated_data.get('updates', instance.updates)
#         instance.deadline  = validated_data.get('deadline', instance.deadline)
#         instance.save()
#         return instance

class UserSerializer(serializers.Serializer):
    username        = serializers.CharField(max_length=50)
    email           = serializers.EmailField(max_length=60)
    profile_picture = serializers.ImageField()
    is_admin        = serializers.BooleanField(default = False)
    is_active       = serializers.BooleanField(default = True)
    is_staff        = serializers.BooleanField(default = False)
    is_superuser    = serializers.BooleanField(default = False)
    date_joined     = serializers.DateTimeField(default=timezone.now)


class Workspaceserializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'


class Todoserializer(serializers.ModelSerializer):
    #workspace = Workspaceserializer()
    class Meta:
        model = ToDo
        fields = '__all__'
        depth = 1

class Notesserializer(serializers.ModelSerializer):
    workspace = Workspaceserializer()
    class Meta:
        model = Notes
        fields = '__all__'

class Journalserializer(serializers.ModelSerializer):
    workspace = Workspaceserializer()
    notes = Notesserializer(many=True)
    class Meta:
        model = Notes
        fields = '__all__'

