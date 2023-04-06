from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Acticle
from .serializers import ActicleSerial
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['GET', 'POST'])
def acticle_list(request):

    if request.method == 'GET':
        acticle_list = Acticle.objects.all()
        serializer = ActicleSerial(acticle_list, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ActicleSerial(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def acticle_detail(request, id):
    try:
        acticle = Acticle.objects.get(id=id)

    except Acticle.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ActicleSerial(acticle)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ActicleSerial(acticle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        acticle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)