from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # 密碼設為 write_only，這樣回傳資料時就不會包含密碼
    password = serializers.CharField(write_only=True)
    # 這邊不用特別寫 username 跟 email 的檢查是因為繼承的模型（ModelSerializer）並指定模型是 User 預設會檢查
    # 但 password 有特殊需求：我們不希望 API 在回傳資料時把使用者的密碼也傳回去（安全性），所以我們必須手動寫出來，加上 write_only=True

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def validate_username(self, value):
        # Django 預設的 ModelSerializer 其實就會自動檢查唯一性 (Unique constraint)
        # 但我們可以在這裡明確寫出來或做更複雜的邏輯
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("這個使用者名稱已經被註冊過了。")
        return value

    def create(self, validated_data):
        # 這裡非常重要：必須使用 create_user 而不是 create
        # 這樣 Django 才會幫你把密碼加密 (Hashing)，不會存明碼
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user