import requests

from django.conf import settings

BASE_URL = settings.EXPRESS_BASE_URL
API_KEY = settings.EXPRESS_API_KEY


def send_sms(phone: str, message: str) -> None:
    """Send an SMS to the customer.

    Args:
        phone(str): The phone number of the customer.
        message(str): The message to be sent.
    """

    url = f"{BASE_URL}/sms/send"

    payload = {
        "api_key": API_KEY,
        "message": message,
        "phone": phone,
    }
    files = []
    headers = {}

    try:
        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files
        )
        print(response.text)

    except Exception as e:
        print(e)
        return


# url = "https://www.expresssms.co.ke/api/sms/send"

# payload = {
#     "api_key": "xxxxxxxxxxxxxxx",
#     "message": "Sample Test Message",
#     "phone": "07xxxxxxxxx",
# }
# files = []
# headers = {}

# response = requests.request("POST", url, headers=headers, data=payload, files=files)

# print(response.text)
