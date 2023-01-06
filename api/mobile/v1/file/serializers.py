from rest_framework import serializers
from app.models import File


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    file_name = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = '__all__'

    def get_file_name(self, obj):
        return obj.file.name
