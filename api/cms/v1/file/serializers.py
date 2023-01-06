from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError
from app.models import File
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


class FileSerializer(serializers.ModelSerializer):
    sid = serializers.UUIDField(read_only=True, )
    created_at = serializers.DateTimeField(read_only=True)
    file = serializers.FileField()

    class Meta:
        model = File
        fields = ('sid', 'file', 'thumbnail', 'created_at', )
