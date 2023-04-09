from django.db.migrations import serializer
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Acticle
from .serializers import ActicleSerial
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.middleware import AuthenticationMiddleware


# Generic View Set API
class GenericViewActicle(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):

    queryset = Acticle.objects.all()
    serializer_class = ActicleSerial
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]


# Using view set too building create and retrieve data
class ActicleViewSet(viewsets.ViewSet):
    def list(self, request):
        acticle_list = Acticle.objects.all()
        serializer = ActicleSerial(acticle_list, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ActicleSerial(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        acticle_set = Acticle.objects.all()
        acticle = get_object_or_404(acticle_set, pk=pk)
        serializer = ActicleSerial(acticle)
        return Response(serializer.data)

    def update(self, request, pk=None):
        acticle = Acticle.objects.get(pk=pk)
        serializer = ActicleSerial(acticle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        acticle = Acticle.objects.get(pk=pk)
        acticle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# generic api views
class GenericApiView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ActicleSerial
    queryset = Acticle.objects.all()

    lookup_field = 'id'

    # Authentication API
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # Authentication by Token
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
