import uuid

from django.db import models


class CylinderStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level_in_percent = models.IntegerField()
    bluetooth_id = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
