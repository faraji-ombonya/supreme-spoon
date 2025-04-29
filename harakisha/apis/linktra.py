import requests
from django.conf import settings

from ..schemas import CylinderInfo

BASE_URL = settings.LINKTRA_BASE_URL
CLIENT_ID = settings.LINKTRA_CLIENT_ID
CLIENT_SECRET = settings.LINKTRA_CLIENT_SECRET


def get_cylinder_info(qr_code: str) -> CylinderInfo | None:
    """
    Get cylinder details from the Linktra API

    Args:
        qr_code(str): The QR Code of the cylinder.
    """

    url = f"{BASE_URL}/cylinder/qr-code/{qr_code}"

    headers = {
        "X-Linktra-ClientId": CLIENT_ID,
        "X-Linktra-ClientSecret": CLIENT_SECRET,
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return None

        print(response.text)
        return response.json()
    except Exception as e:
        print(e)
        return None
