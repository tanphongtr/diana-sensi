import uuid
import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from PIL import Image
from django.core.exceptions import ValidationError
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class MediaStorage(S3Boto3Storage):
    pass


def select_storage():
    return MediaStorage() if os.getenv('USE_S3') else FileSystemStorage()


class FileField(models.FileField):

    def generate_filename(self, instance, filename):
        _, ext = os.path.splitext(filename)
        filename = f'{uuid.uuid4().hex}{ext}'
        return super().generate_filename(instance, filename)


class File(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    file = FileField(upload_to='diana/%Y/%m/%d',)
    # thumbnail = FileField(upload_to='diana/%Y/%m/%d',
    #                       storage=select_storage, default='', null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True, )
    # upload_by = models.ForeignKey('app.User', to_field='sid', db_column='upload_by', null=True, on_delete=models.SET_NULL, related_name='' )
    created_at = models.DateTimeField(
        _("Ngày tạo"), auto_now=True, null=False, )

    class Meta:
        db_table = 'file'
        ordering = ['-id', ]
        verbose_name = _("File")
        verbose_name_plural = _("Files")


def update_file(sender, instance, created, **kwargs):

    if created:
        img = Image.open(instance.file.path)
        if img.height > 300 or img.weight > 300:

            width, height = img.size
            if width == height:
                return img
            offset = int(abs(height-width)/2)
            if width > height:
                img = img.crop([offset, 0, width-offset, height])
            else:
                img = img.crop([0, offset, width, height-offset])
            _, ext = os.path.splitext(instance.file.path)

            new_path_save = f'{_}_thumbnail{ext}'
            _, ext = instance.file.name.split('.')

            new_path_name = f'{_}_thumbnail.{ext}'
            instance.thumbnail = new_path_name

            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(new_path_save)

            instance.save()

# models.signals.post_save.connect(update_file, sender=File, weak=False, dispatch_uid='models.update_file')
