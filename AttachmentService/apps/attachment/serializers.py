from .models import Attachment
from rest_framework import serializers

class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only = True, required = True)
    class Meta:
        model = Attachment
        fields=[
            "id",
            "url",
            "created_at",
            "file"
        ]
        read_only_fields = [
            "id",
            "url",
            "task_id",
            "created_at"
        ]

  #allowing only certain file types to be transferred
    def validate_file(self,value):
        max_size_mb = 5
        if value.size > max_size_mb * 1024 * 1024:
            raise serializers.ValidationError(f"File must be under {max_size_mb}MB")
        
        allowed_types = ["image/jpg", "image/png", "image/webp", "image/jpeg"]

        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only JPEG, PNG, or WEBP files are allowed")
        
        return value