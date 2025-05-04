from rest_framework import serializers

from .models import CylinderStatus, Customer, Cylinder
from .services import allocate_cylinder


class CylinderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CylinderStatus
        fields = "__all__"


class CreateCylinderStatusSerializer(serializers.ModelSerializer):
    levelInPercent = serializers.IntegerField(write_only=True)
    bluetoothId = serializers.CharField(write_only=True)
    serialNumber = serializers.CharField(write_only=True)

    class Meta:
        model = CylinderStatus
        fields = ["levelInPercent", "bluetoothId", "serialNumber"]

    def create(self, validated_data):
        level_in_percent = validated_data.pop("levelInPercent")
        bluetooth_id = validated_data.pop("bluetoothId")
        serial_number = validated_data.pop("serialNumber")
        cylinder_status = CylinderStatus.objects.create(
            level_in_percent=level_in_percent,
            bluetooth_id=bluetooth_id,
            serial_number=serial_number,
        )
        return cylinder_status


class AllocateCylinderSerializer(serializers.ModelSerializer):
    old_qr_code = serializers.CharField(required=False, write_only=True)
    new_qr_code = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = "__all__"

    def create(self, validated_data: dict):
        new_qr_code = validated_data.pop("new_qr_code")
        old_qr_code = validated_data.pop("old_qr_code", None)
        phone_number = validated_data.pop("phone_number")

        # get or create user using phone number
        customer, _ = Customer.objects.get_or_create(
            phone_number=phone_number,
            defaults=validated_data,
        )

        allocate_cylinder(
            old_qr_code=old_qr_code, new_qr_code=new_qr_code, customer_id=customer.id
        )

        return customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
