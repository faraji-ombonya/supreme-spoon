from .apis.linktra import get_cylinder_info
from .apis.express import send_sms
from .models import Cylinder, Customer


def get_or_create_cylinder(qr_code: str) -> Cylinder:
    """Get or create a cylinder.

    Args:
        qr_code(str): QR Code of the cylinder.

    Returns:
        cylinder(Cylinder): An instance of a cylinder.
    """
    cylinder_info = get_cylinder_info(qr_code)

    if not cylinder_info:
        return None

    serial_number = cylinder_info.get("serialNumber")
    bluetooth_id = cylinder_info.get("blueToothId")

    cylinder, _ = Cylinder.objects.get_or_create(
        serial_number=serial_number,
        bluetooth_id=bluetooth_id,
        defaults={
            "cylinder_type": cylinder_info.get("typeOfGas"),
            "size": cylinder_info.get("sizeInLiters"),
            "qr_code": qr_code,
            # "production_date": cylinder_info.get("productionDate"),
        },
    )

    return cylinder


def allocate_cylinder(old_qr_code: str | None, new_qr_code: str, customer_id: str):
    """Allocate a cylinder to a customer.

    Args:
        qr_code(str): The QR Code of the cylinder
        customer_id(str): The ID of the customer
    """

    # Handle new cylinder
    new_cylinder = get_or_create_cylinder(new_qr_code)

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return None

    new_cylinder.customer = customer

    # Handle old cylinder if we have an old QR code
    if old_qr_code:
        old_cylinder = get_or_create_cylinder(old_qr_code)
        old_cylinder.customer = None

    return True


def notify_customer(customer_id: str, message: str):
    """Send a notification to a customer.

    Args:
        customer(Customer): An instance of a customer.
    """
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return None

    send_sms(phone=customer.phone_number, message=message)
