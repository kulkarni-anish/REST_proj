
from django.core import exceptions
from rest_framework import serializers
from .models import MyUser, Notes, ToDo, Workspace
from django.utils import timezone
from drf_writable_nested import WritableNestedModelSerializer
from django.contrib.auth import authenticate



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
        depth = 1                  ##DEPTH

class Notesserializer(WritableNestedModelSerializer,serializers.ModelSerializer):
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



# class LoginSerializer(serializers.Serializer):
#     email           = serializers.EmailField()
#     password        = serializers.CharField()

#     def validate(self, data):
#         email    = data.get("email")
#         password = data.get("password")

#         if email and password:
#             user = authenticate(email=email,password=password)
#             if user:
#                 if user.is_active:
#                     data["user"]= user
#             else:
#                 raise exceptions.ValidationError("Must provide correct email and password")
#         else:
#             raise exceptions.ValidationError("Must provide correct email and password")
        
#         return data


class RegistrationSerializer(serializers.ModelSerializer):

    password2 				= serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
                'password': {'write_only': True},
        }
    def	save(self):
        user = MyUser(
                    email=self.validated_data['email'],
                    username=self.validated_data['username']
                    )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user