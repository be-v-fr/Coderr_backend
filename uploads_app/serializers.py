from rest_framework import serializers
from .models import FileUpload

class FileUploadSerializer(serializers.ModelSerializer):
    """
    A serializer for the FileUpload model.
    """
    class Meta:
        model = FileUpload
        fields = ['file', 'uploaded_at']