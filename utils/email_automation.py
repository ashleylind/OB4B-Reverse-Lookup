import requests
import json

def send_email_via_api(from_address, to_addresses, subject, html):
    """
    Sends an email by calling the Standard Bank internal API endpoint.

    Args:
        from_address (str): Sender email address.
        to_addresses (list[str]): List of recipient email addresses.
        subject (str): Email subject line.
        html (str): HTML or text content of the email.

    Returns:
        dict: JSON response from the API or error message.
    """
    url = "https://psdc-pa002tofv.za.sbicdirectory.com:7443/send-email-local"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "fromAddress": from_address,
        "toAddresses": to_addresses,
        "subject": subject,
        "html": html
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)  # verify=False to skip SSL validation (if using internal certs)
        response.raise_for_status()  # Raise error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


send_email_via_api('BCBFraudIECMTwoBot.IECMTwo@standardbank.co.za', 'bcbfrddtn@standardbank.co.za', 'OB4B Reverse Lookup: The devices has been successfully disabled', "THIS IS A TEST EMAIL")
send_email_via_api('BCBFraudIECMTwoBot.IECMTwo@standardbank.co.za', 'bcbfrddtn@standardbank.co.za', 'OB4B Reverse Lookup: Exception! We failed to disable', "THIS IS A TEST EMAIL")
send_email_via_api('BCBFraudIECMTwoBot.IECMTwo@standardbank.co.za', 'bcbfrddtn@standardbank.co.za', 'OB4B Reverse Lookup: OTP Destination different from system but not in disable criteria', "THIS IS A TEST EMAIL")
send_email_via_api('BCBFraudIECMTwoBot.IECMTwo@standardbank.co.za', 'bcbfrddtn@standardbank.co.za', 'OB4B Reverse Lookup: Device already Disabled', "THIS IS A TEST EMAIL")
