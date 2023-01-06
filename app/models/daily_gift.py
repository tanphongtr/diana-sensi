from django.db import models


class DailyGift(models.Model):
    class BillChoices(models.TextChoices):
        BILL_59 = 'BILL_59', 'BILL_59'
        BILL_79 = 'BILL_79', 'BILL_79'
        BILL_129 = 'BILL_129', 'BILL_129'

    pg_name = models.CharField(max_length=255, null=True, blank=True, )
    pg_phone_number = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    gift = models.ForeignKey('app.Gift', null=True, on_delete=models.SET_NULL,)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    remaining = models.IntegerField(null=True, blank=True, default=0)
    bill = models.CharField(max_length=255, choices=BillChoices.choices, null=True, blank=True, default=None, )

    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_gift'
        verbose_name = 'Daily Gift'
        verbose_name_plural = 'Daily Gifts'
