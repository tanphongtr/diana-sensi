from statistics import mode
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import ulid
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):

    class RoleChoices(models.TextChoices):
        NOROLE = '', _('No role')
        OWNER = 'OWNER', _('Owner')
        SHIPPER = 'SHIPPER', _('Shipper')
        COLLECTOR = 'COLLECTOR', _('Collector')

    class Meta:
        ordering = ['id', ]

    id = models.CharField(max_length=32, primary_key=True,
                          unique=True, default=ulid.new, editable=False)
    sid = models.UUIDField(default=uuid.uuid4, unique=True, null=False)
    phone_number = models.CharField(max_length=255, default='', blank=True, )
    day_of_birth = models.DateField(null=True, )
    full_address = models.CharField(max_length=255, default='', blank=True, )

    def __str__(self):
        return super().get_username()

    """Overide detele()"""

    def delete(self):
        self.is_active = False
        return self.save()

    @property
    def is_owner(self):
        return self.groups.filter(name__contains=self.OWNER).exists()

    @property
    def is_shipper(self):
        return self.groups.filter(name__contains=self.SHIPPER).exists()

    @property
    def is_collector(self):
        return self.groups.filter(name__contains=self.COLLECTOR).exists()
