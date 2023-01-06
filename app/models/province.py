from django.db import models

class Province(models.Model):
    name = models.CharField(max_length=100, )
    code = models.CharField(max_length=255, blank=True, null=True, unique=True, )
    index = models.IntegerField(blank=True, null=True, default=0, )
    hide = models.BooleanField(default=False, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
        ordering = ['index', ]
        db_table = 'province'
