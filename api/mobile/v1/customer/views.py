from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from app.models import Customer
from .serializers import CustomerSerializer
from drf_yasg.utils import swagger_auto_schema
import logging, nanoid

logger = logging.getLogger(__name__)

class CustomerAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @swagger_auto_schema(
        operation_description='Create Customer',
        operation_id='Create Customer',
        operation_summary='Create Customer',
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        _nanoid = nanoid.generate(size=10)
        logger.info(f'{_nanoid} {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f'{_nanoid} CREATED')
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)