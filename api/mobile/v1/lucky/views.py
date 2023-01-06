import json
import random
from rest_framework import generics, viewsets, response
from .serializers import LuckySerializer, GiftSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.models import Gift, DailyGift, daily_gift
from django.utils import timezone
from django.forms.models import model_to_dict
from collections import Counter
import logging
from django.utils import timezone
import nanoid

logger = logging.getLogger(__name__)

class LuckyAPIView(viewsets.ViewSet):
    DONG_HO_DEO_TAY = 'DONG_HO_DEO_TAY'
    LY_THUY_TINH = 'LY_THUY_TINH'
    HOP_BAM_MONG_TAY = 'HOP_BAM_MONG_TAY'
    MAY_LA_TOC = 'MAY_LA_TOC'
    TUI_TOTE = 'TUI_TOTE'
    UNICORN_KHONG_LO = 'UNICORN_KHONG_LO'

    @swagger_auto_schema(
        operation_description="Lucky",
        request_body=LuckySerializer,
    )
    def get_lucky(self, request):
        _nanoid = nanoid.generate(size=10)
        logger.info(f'{_nanoid} {request.data}')

        pg_phone_number = request.data.get('pg_phone_number')
        bill_59 = request.data.get('bill_59')
        bill_79 = request.data.get('bill_79')
        bill_129 = request.data.get('bill_129')

        self.unicorn_khong_lo = request.data.get('unicorn_khong_lo', 0)
        self.may_la_toc = request.data.get('may_la_toc', 0)
        self.tui_tote = request.data.get('tui_tote', 0)
        self.ly_thuy_tinh = request.data.get('ly_thuy_tinh', 0)
        self.dong_ho_deo_tay = request.data.get('dong_ho_deo_tay', 0)
        self.hop_bam_mong_tay = request.data.get('hop_bam_mong_tay', 0)

        daily_gifts = self.get_daily_gifts(pg_phone_number='GIFT_OF_BILL')

        gift_recieved = self.get_gift_for_bill_59(daily_gifts, bill_59)\
            + self.get_gift_for_bill_79(daily_gifts, bill_79)\
            + self.get_gift_for_bill_129(daily_gifts, bill_129)

        # print('gift_recieved', gift_recieved)

        serializer_class = LuckySerializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)

        logger.info(f'{_nanoid} {gift_recieved}')

        return response.Response(gift_recieved, status=200)

    def get_daily_gifts(self, pg_phone_number):
        return DailyGift.objects.filter(
            pg_phone_number=pg_phone_number,
            # date=timezone.now().date(),
        )

    def get_daily_gifts_list(self, daily_gifts):
        final_gifts = []
        for daily_gift in daily_gifts:
            final_gifts += [daily_gift] * daily_gift.remaining

        return final_gifts

    def get_gift_for_bill_59(self, daily_gifts, qty):
        # Nếu có qty và remaining > 0 thì trả về gift
        for daily_gift in daily_gifts:
            # if daily_gift.gift.code == self.DONG_HO_DEO_TAY\
            if daily_gift.gift.code == self.HOP_BAM_MONG_TAY\
                and int(self.hop_bam_mong_tay) > 0\
                and qty > 0:
                return [{
                    'gift': {
                        'code': daily_gift.gift.code,
                        'name': daily_gift.gift.name,
                        'id': daily_gift.gift.id
                    },
                    'quantity': qty,
                }]

        return []

    def get_gift_for_bill_79(self, daily_gifts, qty):
        final_gifts = []

        for daily_gift in daily_gifts:

            if daily_gift.gift.code == self.LY_THUY_TINH:
                final_gifts += [daily_gift] * int(self.ly_thuy_tinh)

            if daily_gift.gift.code == self.DONG_HO_DEO_TAY:
                final_gifts += [daily_gift] * int(self.dong_ho_deo_tay)

        gifts = []

        # print('get_gift_for_bill_79___final_gifts', final_gifts)

        for i in range(qty):
            # print('final_gifts', final_gifts)

            if len(final_gifts):
                gift = random.choices(final_gifts)
                final_gifts.remove(gift[0])

                gifts += [gift[0]]

        a = []
        for k, v in Counter(gifts).items():
            a.append({
                'gift': {
                    'code': k.gift.code,
                    'name': k.gift.name,
                    'id': k.gift.id,
                },
                'quantity': v,
            })

        return a

    def get_gift_for_bill_129(self, daily_gifts, qty):
        final_gifts = []

        for daily_gift in daily_gifts:

            if daily_gift.gift.code == self.TUI_TOTE:
                final_gifts += [daily_gift] * int(self.tui_tote)

            if daily_gift.gift.code == self.MAY_LA_TOC:
                final_gifts += [daily_gift] * int(self.may_la_toc)

            if daily_gift.gift.code == self.UNICORN_KHONG_LO:
                final_gifts += [daily_gift] * int(self.unicorn_khong_lo)

        gifts = []

        # print('get_gift_for_bill_129___final_gifts', final_gifts)
        for i in range(qty):

            if len(final_gifts):
                gift = random.choices(final_gifts)
                final_gifts.remove(gift[0])
                gifts += [gift[0]]
        a = []
        for k, v in Counter(gifts).items():
            a.append({
                'gift': {
                    'code': k.gift.code,
                    'name': k.gift.name,
                    'id': k.gift.id,
                },
                'quantity': v,
            })
        return a
