from .apis import get_cylinder_info
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
    bluetooth_id = cylinder_info.get("bluetoothId")

    cylinder, _ = Cylinder.objects.get_or_create(
        serial_number=serial_number,
        bluetooth_id=bluetooth_id,
        defaults={
            "cylinder_type": cylinder_info.get("typeOfGas"),
            "size": cylinder_info.get("sizeInLiters"),
            "qr_code": qr_code,
            "production_date": cylinder_info.get("productionDate"),
        },
    )

    return cylinder


def allocate_cylinder(old_qr_code: str, new_qr_code: str, customer_id: str):
    """Allocate a cylinder to a customer.

    Args:
        qr_code(str): The QR Code of the cylinder
        customer_id(str): The ID of the customer
    """

    new_cylinder = get_or_create_cylinder(new_qr_code)
    old_cylinder = get_or_create_cylinder(old_qr_code)

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return None

    new_cylinder.customer = customer
    old_cylinder.customer = None

    return True
