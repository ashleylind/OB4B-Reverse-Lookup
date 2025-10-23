from utils.email_automation import send_email_via_api
import time
from tqdm import tqdm

import pandas as pd

def process_email_statuses(excel_path, logger):
    """
    Reads an Excel file and sends an email based on each row's Status.
    """
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        logger.info(f"Error reading Excel file: {e}")
        return

    # Normalize column names (in case of extra spaces)
    df.columns = df.columns.str.strip()

    for index, row in tqdm(df.iterrows()):
        status = str(row.get("Status", "")).strip()
        digital_id = str(row.get("Digital ID", "")).strip()
        otp_destination = str(row.get("OTP Destination", "")).strip()
        timestamp = str(row.get("Timestamp", "")).strip()

        logger.info(f"Processing row {index}: Digital ID={digital_id}, Status={status}")

        # Choose subject based on Status
        if status == "Different OTP Destination, not in disable criteria":
            status = "Not in Disable criteria"
            subject = "OB4B Reverse Lookup: OTP Destination different from system but not in disable criteria"
        elif status == "Error":
            subject = "OB4B Reverse Lookup: Exception! We failed to disable"
        elif status == "Disabled":
            subject = "OB4B Reverse Lookup: The device has been successfully disabled"
        elif status == "Already Disabled":
            subject = "OB4B Reverse Lookup: Device already Disabled"
        else:
            # Skip unknown statuses
            logger.info(f"Skipping row {index} — Unknown status: {status}")
            continue

        # Email details
        from_address = "BCBFraudIECMTwoBot.IECMTwo@standardbank.co.za"
        to_address = ["bcbfrddtn@standardbank.co.za", "BCBFraudIECMTwoBot.IECMTwo@standardbank.co.za"]
        html_message = (
            f"<p>Digital ID: <b>{digital_id}</b></p>"
            f"<p>OTP Destination: <b>{otp_destination}</b></p>"
            f"<p>Status: <b>{status}</b></p>"
        )

        # Call the API
        try:
            time.sleep(2)
            response = send_email_via_api(from_address, to_address, subject, html_message)
            logger.info(f" Email sent for row {index}: {status}")
        except Exception as e:
            logger.info(f" Failed to send email for row {index}: {e}")


