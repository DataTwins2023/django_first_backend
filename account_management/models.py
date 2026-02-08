from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    # 使用 UUID 作為主鍵（就像你 Document 模型做的一樣，更安全）
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Django AbstractUser 內建已有 username, password, email 等欄位
    # 如果有特殊需求再加在這裡

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username