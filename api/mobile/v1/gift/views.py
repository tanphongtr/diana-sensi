from rest_framework import generics
from .serializers import GiftSerializer
from app.models import Gift
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.common.paginations import StandardResultsSetPagination


swagger_tags = ['Gift']


class GiftAPIView(generics.ListAPIView):
    serializer_class = GiftSerializer
    queryset = Gift.objects.all()
    pagination_class = StandardResultsSetPagination
    pagination_class.page_size = 1000

    def get_queryset(self):
        return Gift.objects.filter(hide=False)

    @swagger_auto_schema(
        tags=swagger_tags,
        operation_description='',
        operation_id='List Gifts',
        operation_summary='',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)