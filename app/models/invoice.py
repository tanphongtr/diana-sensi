from django.db import models


class Invoice(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, )

    code = models.CharField(max_length=255, blank=True,
                            null=True, unique=True, )

    customer = models.ForeignKey(
        'app.Customer', on_delete=models.CASCADE, blank=True, null=True, related_name='invoices', )

    created_at = models.DateTimeField(auto_now_add=True, )
    last_update = models.DateTimeField(auto_now=True, )

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['created_at', ]
        db_table = 'invoice'


class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(
        'app.Invoice', on_delete=models.CASCADE, blank=True, null=True, related_name='products', )
    product = models.ForeignKey(
        'app.Product', on_delete=models.PROTECT, blank=True, null=True, related_name='products', )

    quantity = models.IntegerField(blank=True, null=True, default=0, )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, )

    created_at = models.DateTimeField(auto_now_add=True, )
    last_update = models.DateTimeField(auto_now=True, )

    class Meta:
        verbose_name = 'Invoice Product'
        verbose_name_plural = 'Invoice Products'
        ordering = ['created_at', ]
        db_table = 'invoice_product'

    # def save(self, *args, **kwargs):
    #     self.price = self.product.price
    #     self.total = self.quantity * self.price
    #     super().save(*args, **kwargs)


class InvoiceGift(models.Model):
    invoice = models.ForeignKey(
        'app.Invoice', on_delete=models.CASCADE, blank=True, null=True, related_name='gifts', )
    gift = models.ForeignKey(
        'app.Gift', on_delete=models.PROTECT, blank=True, null=True, related_name='gifts', )

    quantity = models.IntegerField(blank=True, null=True, default=0, )
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, )

    created_at = models.DateTimeField(auto_now_add=True, )
    last_update = models.DateTimeField(auto_now=True, )

    class Meta:
        verbose_name = 'Invoice Gift'
        verbose_name_plural = 'Invoice Gifts'
        ordering = ['created_at', ]
        db_table = 'invoice_gift'

    # def save(self, *args, **kwargs):
    #     print('self.gift', self.gift.value)
    #     self.value = self.gift.value
    #     self.total = self.quantity * self.value
    #     super().save(*args, **kwargs)

def __update_invoice_total(instance, **kwargs):
    from django.db.models import Sum
    invoice = instance.invoice
    invoice.total = InvoiceProduct.objects.filter(
        invoice=invoice).aggregate(Sum('total')).get('total__sum') or int(0)
    invoice.save()

def __post_save(sender, instance, created, **kwargs):
    __update_invoice_total(instance)

def __post_delete(sender, instance, using, **kwargs):
    __update_invoice_total(instance)

# models.signals.post_save.connect(__post_save, sender=InvoiceProduct, weak=False, dispatch_uid='models.update_invoice')
# models.signals.post_delete.connect(__post_delete, sender=InvoiceProduct, weak=False, dispatch_uid='models.update_invoice')