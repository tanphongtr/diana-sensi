from rest_framework import generics
from .serializers import ProductSerializer
from app.models import Product
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.common.paginations import StandardResultsSetPagination


swagger_tags = ['Product']


class ProductAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = StandardResultsSetPagination
    pagination_class.page_size = 1000

    def get_queryset(self):
        return Product.objects.filter(hide=False)

    @swagger_auto_schema(
        tags=swagger_tags,
        operation_description='',
        operation_id='List Products',
        operation_summary='',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
