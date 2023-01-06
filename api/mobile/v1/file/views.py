from rest_framework import generics
from app.models import File
from .serializers import FileSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser



class FileAPIView(generics.CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
