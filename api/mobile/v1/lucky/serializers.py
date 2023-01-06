from rest_framework import serializers
from app.models import Gift, DailyGift


class LuckySerializer(serializers.Serializer):
    pg_phone_number = serializers.CharField(max_length=255, required=True)
    bill_59 = serializers.IntegerField()
    bill_79 = serializers.IntegerField()
    bill_129 = serializers.IntegerField()

    unicorn_khong_lo = serializers.IntegerField()
    may_la_toc = serializers.IntegerField()
    tui_tote = serializers.IntegerField()
    hop_bam_mong_tay = serializers.IntegerField()
    ly_thuy_tinh = serializers.IntegerField()
    dong_ho_deo_tay = serializers.IntegerField()


    def validate(self, attrs):
        return attrs

class GiftSerializer(serializers.ModelSerializer):

    class Meta:
        models = Gift
        fields = '__all__'
