from django.db import models


class Market(models.Model):
    name = models.CharField(max_length=100, )
    code = models.CharField(max_length=255, blank=True, null=True, unique=True, )
    index = models.IntegerField(blank=True, null=True, default=0, )
    hide = models.BooleanField(default=False, )

    # Related fields
    system = models.ForeignKey(
        'app.System', on_delete=models.PROTECT, blank=True, null=True, related_name='markets', )

    def __str__(self):
        if self.system:
            return '%s - %s' % (self.name, self.system.name)
        return self.name

    class Meta:
        verbose_name = 'Market'
        verbose_name_plural = 'Markets'
        ordering = ['index', ]
        db_table = 'market'
