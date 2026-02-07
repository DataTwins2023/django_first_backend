from django.db import models
from django.db.models import UniqueConstraint
import uuid
# Create your models here.

class Document(models.Model):
    document_id = models.UUIDField(primary_key=True, default=uuid.uuid4, blank = False, editable=False)
    file_name = models.CharField(max_length=255, null = True, blank = True)
    display_name = models.CharField(max_length=255, null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'document'
        indexes = [
            models.Index(fields=["-updated_at"]),
            models.Index(fields=["created_at"])
        ]

    def __str__(self):
        return f"Document {self.file_name}"
    