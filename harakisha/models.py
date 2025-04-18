import uuid

from django.db import models


class CylinderStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level_in_percent = models.IntegerField()
    bluetooth_id = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cylinder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serial_number = models.CharField(max_length=100)
    level_in_percent = models.IntegerField()
    bluetooth_id = models.CharField(max_length=100)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="cylinders"
    )
    cylinder_type = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    qr_code = models.CharField(max_length=100)
    production_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
