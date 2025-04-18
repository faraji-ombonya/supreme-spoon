from rest_framework import serializers

from .models import CylinderStatus, Customer, Cylinder


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
    qr_code = serializers.CharField()

    class Meta:
        model = Customer
        fields = "__all__"

    def create(self, validated_data):
        qr_code = validated_data.pop("qr_code")
        phone_number = validated_data.pop("phone_number")

        # get or create user using phone number
        customer, created = Customer.objects.get_or_create(
            phone_number=phone_number,
            defaults=validated_data,
        )

        return customer
