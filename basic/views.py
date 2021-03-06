import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers, status
from rest_framework import generics, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from basic.email import send_mail
from .models import MyUser, ToDo, Notes
from .serializers import RegistrationSerializer, Todoserializer, Notesserializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


# Create your views here.

#@csrf_exempt
@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todos = ToDo.objects.all()
        serializer = Todoserializer(todos, many=True)
        #return JsonResponse(serializer.data, safe=False)  ##Find out why
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Todoserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            #return JsonResponse(serializer.data, status=201) #created
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        #return JsonResponse(serializer.errors, status=400) #bad request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['GET', 'PUT', 'DELETE'])
def todo_view(request, pk):
    try:
        todo = ToDo.objects.get(pk=pk)
    except ToDo.DoesNotExist:
        return HttpResponse(status=404) 

    if request.method == 'GET':
        serializer = Todoserializer(todo)
        #return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = Todoserializer(todo, data=data)
        if serializer.is_valid():
            serializer.save()
            #return JsonResponse(serializer.data)
            return Response(serializer.data)

        return JsonResponse(serializer.errors, status=400) #bad request

    elif request.method == 'DELETE':
        todo.delete()
        return HttpResponse(status=204) #no content



class NotesList(generics.ListCreateAPIView):
    queryset = Notes.objects.all()
    serializer_class = Notesserializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notes.objects.all()
    serializer_class = Notesserializer

@api_view(['POST', ])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()

            send_mail(html=None,
                text='Here is your Confirmation',
                subject='Confirmationtoken',
                from_email='djangorest3@gmail.com',
                to_emails=[user.email])

            data['response'] = 'successfully registered new user.'
            data['email'] = user.email
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


# @api_view(['POST'])
# def registration_view(request,tok):
#     if request.method == 'POST':
#         serializer = RegistrationSerializer(data=request.data)
#         data = {}
#         email = request.data['email']
#         if serializer.is_valid():
#             send_mail(html=None,
#                 text='Here is your Confirmation',
#                 subject='Confirmationtoken',
#                 from_email='djangorest3@gmail.com',
#                 to_emails=[email])

# @api_view(['GET', ])
# def confirmation_view(request):


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer