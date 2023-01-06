from django.db import models


class Product(models.Model):

    class CodeChoices(models.TextChoices):
        SENSI_8M = 'SENSI_8M', 'SENSI_8M'
        SENSI_20M = 'SENSI_20M', 'SENSI_20M'

    name = models.CharField(max_length=100, )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, )
    code = models.CharField(max_length=255, blank=True, null=True, unique=True, )
    index = models.IntegerField(blank=True, null=True, default=0, )
    hide = models.BooleanField(default=False, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['index', ]
        db_table = 'product'
