from rest_framework import serializers

from .models import CylinderStatus, Customer, Cylinder, Order
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


"""
{
  "transactionId":   "string",   // Wix’s unique order ID
  "paymentStatus":   "paid"|"unpaid",
  "customer": {
    "email":        "string",
    "firstName":    "string",
    "lastName":     "string",
    "phoneNumber":  "string",
    "country":      "string",
    "addressLine1": "string",
    "addressLine2": "string",     // optional
    "city":         "string",
    "postalCode":   "string"
  },
  "productType":     "string",   // e.g. “13 kg cooking cylinder”
  "purchaseDate":    "2025-05-06T14:30:00Z"
}
"""


class PseudoCustomerSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    firstName = serializers.CharField(required=False)
    lastName = serializers.CharField(required=False)
    phoneNumber = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    addressLine1 = serializers.CharField(required=False)
    addressLine2 = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    postalCode = serializers.CharField(required=False)

    def create(self, validated_data):
        # extract customer data
        customer_data = {
            "email": validated_data.get("email", None),
            "first_name": validated_data.get("firstName", None),
            "last_name": validated_data.get("lastName", None),
            "phone_number": validated_data.get("phoneNumber", None),
            "country": validated_data.get("country", None),
            "address_line_1": validated_data.get("addressLine1", None),
            "city": validated_data.get("city", None),
            "postal_code": validated_data.get("postalCode", None),
        }

        # Create a customer instance
        try:
            phone_number = customer_data.pop("phone_number", None)
            customer_instance, _ = Customer.objects.get_or_create(
                phone_number=phone_number,
                defaults=customer_data,
            )
        except Exception as e:
            print("Error creating customer", str(e))
            pass

        return customer_instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class CreateOrderSerializer(serializers.Serializer):
    transactionId = serializers.CharField(required=False)
    paymentStatus = serializers.CharField(required=False)
    customer = PseudoCustomerSerializer(required=False)
    productType = serializers.CharField(required=False)
    purchaseDate = serializers.DateTimeField(required=False)

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data: dict):
        order_data = {
            "wix_transaction_id": validated_data.get("transactionId", None),
            "payment_status": validated_data.get("paymentStatus", None),
            "product_type": validated_data.get("productType", None),
            "purchase_date": validated_data.get("purchaseDate", None),
        }

        # extract customer data
        customer_data: dict = validated_data.pop("customer", None)
        if customer_data:
            customer_serializer = PseudoCustomerSerializer(data=customer_data)
            customer_serializer.is_valid(raise_exception=True)
            customer_instance = customer_serializer.save()

        order_instance = Order.objects.create(**order_data, customer=customer_instance)
        return order_instance


class OrderResponseSerializer(serializers.Serializer):
    status = serializers.CharField(default="order recorded")
    orderId = serializers.UUIDField(source="id")
