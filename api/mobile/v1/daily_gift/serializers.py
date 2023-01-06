from rest_framework import serializers
from app.models import DailyGift, Gift
from django.utils import timezone

class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = '__all__'

class DailyGiftSerializer(serializers.ModelSerializer):
    _pre_name = serializers.SerializerMethodField()
    gift = GiftSerializer()
    class Meta:
        model = DailyGift
        fields = '__all__'

    def get__pre_name(self, obj):
        if obj.gift.code == Gift.CodeChoices.HOP_BAM_MONG_TAY.value:
            return f'Bill 59.000 - {obj.gift.name}'

        if obj.gift.code == Gift.CodeChoices.LY_THUY_TINH.value\
            or obj.gift.code == Gift.CodeChoices.DONG_HO_DEO_TAY.value:
            return f'Bill 79.000 - {obj.gift.name}'

        if obj.gift.code == Gift.CodeChoices.MAY_LA_TOC.value\
            or obj.gift.code == Gift.CodeChoices.TUI_TOTE.value\
            or obj.gift.code == Gift.CodeChoices.UNICORN_KHONG_LO.value:
            return f'Bill 129.000 - {obj.gift.name}'

        return None

class _DailyGiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyGift
        fields = ('gift', 'quantity', )

class POSTDailyGiftSerializer(serializers.Serializer):
    pg_name = serializers.CharField(max_length=255, required=False,)
    pg_phone_number = serializers.CharField(max_length=20)
    daily_gifts = _DailyGiftSerializer(many=True, write_only=True, )

    def create(self, validated_data):
        pg_name = validated_data.pop('pg_name')
        pg_phone_number = validated_data.pop('pg_phone_number')
        daily_gifts = validated_data.pop('daily_gifts')

        __daily_gifts = []
        for daily_gift in daily_gifts:

            bill = None
            
            if daily_gift['gift'].code == Gift.CodeChoices.HOP_BAM_MONG_TAY.value:
                bill = DailyGift.BillChoices.BILL_59.value

            if daily_gift['gift'].code == Gift.CodeChoices.DONG_HO_DEO_TAY.value\
                or daily_gift['gift'].code == Gift.CodeChoices.LY_THUY_TINH.value:
                bill = DailyGift.BillChoices.BILL_79.value

            if daily_gift['gift'].code == Gift.CodeChoices.TUI_TOTE.value\
                or daily_gift['gift'].code == Gift.CodeChoices.MAY_LA_TOC.value\
                or daily_gift['gift'].code == Gift.CodeChoices.UNICORN_KHONG_LO.value:
                bill = DailyGift.BillChoices.BILL_129.value

            __daily_gift, _ = DailyGift.objects.update_or_create(
                pg_phone_number=pg_phone_number,
                gift=daily_gift['gift'],
                date=timezone.now().date(),
                defaults={
                    'pg_name': pg_name,
                    'bill': bill,
                    'quantity': daily_gift['quantity'],
                    'remaining': daily_gift['quantity'],
                }
            )
            __daily_gifts.append(__daily_gift)
        return __daily_gifts


class BillListSerializer(serializers.Serializer):

    pg_number_phone = serializers.CharField(max_length=20)
