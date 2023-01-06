from rest_framework import generics


class APIView(generics.ListCreateAPIView):
    pass


class DetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass