from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import ToDo
from .serializers import Todoserializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = Todoserializer(todo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400) #bad request

    elif request.method == 'DELETE':
        todo.delete()
        return HttpResponse(status=204) #no content