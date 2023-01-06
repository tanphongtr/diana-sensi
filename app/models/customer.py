from venv import create
from django.db import models

from app.models import survey

class Customer(models.Model):

    # PG fields
    pg_name = models.CharField(max_length=100)
    pg_phone_number = models.CharField(max_length=100)

    # Location fields
    market = models.ForeignKey('app.Market', on_delete=models.PROTECT,)

    # Customer fields
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    invoice_photo = models.ImageField(upload_to='diana/%Y/%m/%d', blank=True, null=True, )

    created_at = models.DateTimeField(auto_now_add=True, )
    last_update = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['-id', ]
        # db_table = 'customer'


class CustomerV2(Customer):
    class Meta:
        proxy = True
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers v2'

class CustomerV3(Customer):
    class Meta:
        proxy = True
        verbose_name = 'View Invoice'
        verbose_name_plural = 'View Invoices'