from django.db import models


class System(models.Model):
    name = models.CharField(max_length=100, )
    code = models.CharField(max_length=255, blank=True, null=True, unique=True, )
    index = models.IntegerField(blank=True, null=True, default=0, )
    hide = models.BooleanField(default=False, )

    # Related fields
    province = models.ForeignKey(
        'app.Province', on_delete=models.PROTECT, blank=True, null=True, related_name='systems', )

    def __str__(self):
        if self.province:
            return '%s - %s' % (self.name, self.province.name)
        return self.name

    class Meta:
        db_table = 'system'
        verbose_name = 'System'
        verbose_name_plural = 'Systems'
        ordering = ['index', ]


