from django.db import models


class Gift(models.Model):

    class CodeChoices(models.TextChoices):
        DONG_HO_DEO_TAY = 'DONG_HO_DEO_TAY', 'DONG_HO_DEO_TAY'
        HOP_BAM_MONG_TAY = 'HOP_BAM_MONG_TAY', 'HOP_BAM_MONG_TAY'
        LY_THUY_TINH = 'LY_THUY_TINH', 'LY_THUY_TINH'
        TUI_TOTE = 'TUI_TOTE', 'TUI_TOTE'
        MAY_LA_TOC = 'MAY_LA_TOC', 'MAY_LA_TOC'
        UNICORN_KHONG_LO = 'UNICORN_KHONG_LO', 'UNICORN_KHONG_LO'

    name = models.CharField(max_length=100, )
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, )
    code = models.CharField(max_length=255, blank=True, null=True, unique=True, )
    index = models.IntegerField(blank=True, null=True, default=0, )
    hide = models.BooleanField(default=False, )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'gift'
        verbose_name = 'Gift'
        verbose_name_plural = 'Gifts'
        ordering = ['index', ]
