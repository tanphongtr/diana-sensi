from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from app.models import DailyGift, Gift
from .serializers import DailyGiftSerializer, POSTDailyGiftSerializer, BillListSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
import logging, nanoid

logger = logging.getLogger(__name__)


class DailyGiftAPIView(generics.ListCreateAPIView):
    queryset = DailyGift.objects.all()
    serializer_class = DailyGiftSerializer
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    filterset_fields = {
        'pg_phone_number': ['exact'],
    }
    def get_queryset(self):
        queryset = DailyGift.objects.filter(date=timezone.now().date())
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return POSTDailyGiftSerializer
        return DailyGiftSerializer

    def perform_create(self, serializer):
            return serializer.save()

    @swagger_auto_schema(
        operation_description='Post Daily Gifts',
        operation_id='Post Daily Gifts',
        operation_summary='Post Daily Gifts',
    )
    def post(self, request, *args, **kwargs):
        _nanoid = nanoid.generate(size=10)
        logger.info(f'{_nanoid} {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        serializer = DailyGiftSerializer(instance, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BillListAPIView(viewsets.ViewSet):
    def bill_list(self, request):
        daily_gifts = DailyGift.objects.filter(
            pg_phone_number=request.data.get('pg_phone_number'),
            date=timezone.now().date()
        )

        bill_list = []

        for daily_gift in daily_gifts:
            if daily_gift.gift.code == Gift.CodeChoices.DONG_HO_DEO_TAY.value\
                and daily_gift.remaining <= 0:
                bill_list.append({
                    'bill': 'bill_59',
                    'disable': True
                })

            if (daily_gift.gift.code == Gift.CodeChoices.HOP_BAM_MONG_TAY.value\
                or daily_gift.gift.code == Gift.CodeChoices.LY_THUY_TINH.value)\
                and daily_gift.gift.code == daily_gift.remaining <= 0:
                bill_list.append({
                    'bill': 'bill_79',
                    'disable': True
                })

            if (daily_gift.gift.code == Gift.CodeChoices.MAY_LA_TOC.value\
                or daily_gift.gift.code == Gift.CodeChoices.TUI_TOTE.value\
                or daily_gift.gift.code == Gift.CodeChoices.UNICORN_KHONG_LO.value)\
                and daily_gift.gift.code == daily_gift.remaining <= 0:
                bill_list.append({
                    'bill': 'bill_129',
                    'disable': True
                })
        return Response(bill_list, status=200)