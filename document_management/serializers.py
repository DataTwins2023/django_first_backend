from rest_framework import serializers

class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField(required=True, help_text="File to upload")
    display_name = serializers.CharField(required=False, help_text="like Finance")
    description = serializers.CharField(required=False, help_text="Description of the file")  

    def validate_file(self, value):
        max_size = 5 * 1024 * 1024  # 5MB 
        if value.size > max_size:
            raise serializers.ValidationError(f"File size should not exceed {max_size} bytes.")
        return value
    
    def validate_display_name(self, value):
        if value and len(value) > 255:
            raise serializers.ValidationError("Display name should not exceed 255 characters.")
        return value
    
    def validate_description(self, value):
        if value and len(value) > 1000:
            raise serializers.ValidationError("Description should not exceed 1000 characters.")
        return value
    
class PartialUpdateSerializer(serializers.Serializer):
    file = serializers.FileField(required=False, help_text="File to upload")
    display_name = serializers.CharField(required=False, help_text="like Finance")
    description = serializers.CharField(required=False, help_text="Description of the file") 

    def validate_file(self, value):
        max_size = 5 * 1024 * 1024  # 5MB 
        if value and value.size > max_size:
            raise serializers.ValidationError(f"File size should not exceed {max_size} bytes.")
        return value
    
    def validate_display_name(self, value):
        if value and len(value) > 255:
            raise serializers.ValidationError("Display name should not exceed 255 characters.")
        return value
    
    def validate_description(self, value):
        if value and len(value) > 1000:
            raise serializers.ValidationError("Description should not exceed 1000 characters.")
        return value
    
    def update(self, instance, validated_data):
        # 1. 處理檔案相關邏輯
        file_obj = validated_data.get('file')
        if file_obj:
            # 如果你有用 FileField，直接 instance.file = file_obj
            # 如果你只是要存名字字串：
            instance.file_name = file_obj.name

        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    

