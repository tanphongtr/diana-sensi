from rest_framework import serializers, generics
from app.models import Province, System, Market
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.common.paginations import StandardResultsSetPagination
from rest_framework import filters
import django_filters.rest_framework

swagger_tags = ['Common']

################################################################################
# Province
################################################################################


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class ProvinceAPIView(generics.ListAPIView):
    serializer_class = ProvinceSerializer
    queryset = Province.objects.all()
    pagination_class = StandardResultsSetPagination
    pagination_class.page_size = 1000

    def get_queryset(self):
        return Province.objects.filter(hide=False)

    @swagger_auto_schema(
        tags=swagger_tags,
        operation_description='',
        operation_id='List Provinces',
        operation_summary='',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


################################################################################
# System
################################################################################

class SystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = System
        fields = '__all__'


class SystemAPIView(generics.ListAPIView):
    serializer_class = SystemSerializer
    queryset = System.objects.all()
    pagination_class = StandardResultsSetPagination
    pagination_class.page_size = 1000
    filter_backends = (filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend)
    filterset_fields = {
        'province': ['exact'],
        'province__code': ['exact'],
    }

    def get_queryset(self):
        return System.objects.filter(hide=False)

    @swagger_auto_schema(
        tags=swagger_tags,
        operation_description='',
        operation_id='List Systems',
        operation_summary='',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


################################################################################
# Market
################################################################################

class MarketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Market
        fields = '__all__'


class MarketAPIView(generics.ListAPIView):
    serializer_class = MarketSerializer
    queryset = Market.objects.all()
    pagination_class = StandardResultsSetPagination
    pagination_class.page_size = 1000
    filter_backends = (filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend)
    filterset_fields = {
        'system': ['exact'],
        'system__code': ['exact'],
    }

    def get_queryset(self):
        return Market.objects.filter(hide=False)

    @swagger_auto_schema(
        tags=swagger_tags,
        operation_description='',
        operation_id='List Markets',
        operation_summary='',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


################################################################################
# Cascade
################################################################################


class SystemSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)

    class Meta:
        model = System
        fields = '__all__'


class ProvinceSystemMarketSerializer(serializers.ModelSerializer):
    systems = SystemSerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = '__all__'


class ProvinceSystemMarketAPIView(generics.ListAPIView):
    serializer_class = ProvinceSystemMarketSerializer
    queryset = Province.objects.all()
    pagination_class = StandardResultsSetPagination
    pagination_class.page_size = 1000

    def get_queryset(self):
        return Province.objects.filter(hide=False)

    @swagger_auto_schema(
        tags=swagger_tags,
        operation_description='',
        operation_id='List Provinces, Systems and Markets',
        operation_summary='',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
