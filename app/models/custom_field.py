from email.policy import default
import os
import uuid, ulid
from django.db import models
from django.utils.translation import gettext_lazy as _


class UnsignedAutoField(models.AutoField):
    def db_type(self, connection):
        return 'integer UNSIGNED AUTO_INCREMENT'

    def rel_db_type(self, connection):
        return 'integer UNSIGNED'

class UnsignedBigAutoField(models.BigAutoField):
    def db_type(self, connection):
        return 'integer UNSIGNED AUTO_INCREMENT'

    def rel_db_type(self, connection):
        return 'integer UNSIGNED'

class FileField(models.FileField):
    def generate_filename(self, instance, filename):
        _, ext = os.path.splitext(filename)
        filename = f'{uuid.uuid4().hex}{ext}'
        return super().generate_filename(instance, filename)

class CImageField(models.ImageField):
    def generate_filename(self, instance, filename):
        _, ext = os.path.splitext(filename)
        filename = f'{uuid.uuid4().hex}{ext}'
        return super().generate_filename(instance, filename)

class ULIDField(models.Field):
    pass
