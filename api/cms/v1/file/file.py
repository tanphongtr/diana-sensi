from os import name
from rest_framework import generics, status
from app.models import File
from .serializers import FileSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.authentication import BaseAuthentication, BasicAuthentication, SessionAuthentication

class FileAPIView(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser,)
    
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class FileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'sid'
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
