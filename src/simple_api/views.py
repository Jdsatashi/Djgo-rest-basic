from django.db.migrations import serializer
from django.shortcuts import render
from django.http import HttpResponse
from .models import Acticle
from .serializers import ActicleSerial
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.views import APIView


# generic api views
class GenericApiView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ActicleSerial
    queryset = Acticle.objects.all()

    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


# API view of Dj-REST framework, this has GET and POST methods
class acticleAPIView(APIView):
    def get(self, request):
        acticle_list = Acticle.objects.all()
        serializer = ActicleSerial(acticle_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActicleSerial(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API View of Dj-REST framework for PUT, GET PK/ID and DELETE methods
class acticleDetails(APIView):
    def get_object(self, id):
        try:
            return Acticle.objects.get(id=id)
        except Acticle.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        acticle = self.get_object(id)
        serializer = ActicleSerial(acticle)
        return Response(serializer.data)

    def put(self, request, id):
        acticle = self.get_object(id)
        serializer = ActicleSerial(acticle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        acticle = self.get_object(id)
        acticle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Use regular view Django's HTTP request
@api_view(['GET', 'POST'])
def acticle_list(request):
    # method GET to show all acticles
    if request.method == 'GET':
        acticle_list = Acticle.objects.all()
        serializer = ActicleSerial(acticle_list, many=True)
        return Response(serializer.data)
    # method POST to create acticle
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
