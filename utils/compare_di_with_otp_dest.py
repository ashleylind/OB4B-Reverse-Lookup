import pandas as pd
import time
import requests
import urllib3
import os
import sqlite3
from datetime import datetime

# Disable SSL warnings for internal HTTPS calls
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def compare_di_with_otp(logger):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # --- File paths ---
    csv_path = r"C:\Users\C900801\Downloads\Enroll OTP.csv"
    matched_path = fr"C:\Users\C900801\OneDrive - Standard Bank\Documents\Reverse_Lookup_Reports\Matched_OTP_{timestamp}.xlsx"
    unmatched_path = fr"C:\Users\C900801\OneDrive - Standard Bank\Documents\Reverse_Lookup_Reports\Unmatched_OTP_{timestamp}.xlsx"
    exceptions_path = fr"C:\Users\C900801\OneDrive - Standard Bank\Documents\Reverse_Lookup_Reports\Exceptions_OTP_{timestamp}.xlsx"
    db_path = fr"C:\Users\C900801\OneDrive - Standard Bank\Documents\reverse_lookup_tracking.db"

    # --- Setup SQLite ---
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS obfourb_reverse_lookup (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            processed_key TEXT UNIQUE
        )
    """)
    conn.commit()

    # --- Read CSV ---
    try:
        df = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines="skip")
        logger.info(f"[INFO] Successfully loaded CSV: {csv_path}")

        # Remove duplicate @digitalId values
        if "@digitalId" in df.columns:
            original_count = len(df)
            df = df.drop_duplicates(subset="@digitalId", keep="first")
            removed_count = original_count - len(df)
            logger.info(f"[INFO] Removed {removed_count} duplicate rows based on '@digitalId' column.")
        else:
            logger.info("[WARNING] '@digitalId' column not found — skipping duplicate removal.")

    except Exception as e:
        if logger:
            logger.error(f"[ERROR] Reading CSV file failed: {e}")
        else:
            logger.info(f"[ERROR] Reading CSV file failed: {e}")
        return

    matched_rows = []
    unmatched_rows = []
    exception_rows = []

    # --- Loop through each record ---
    for index, row in df.iterrows():
        di = str(row.get("@digitalId", "")).strip()
        raw_ts = str(row.get("@timestamp", "")).strip()
        # try:
        #     ts_obj = datetime.strptime(raw_ts, "%H:%M:%S.%f")  # parse '12:45:51.977'
        #     timestamp_from_kibana = ts_obj.strftime("%H:%M")    # get '12:45'
        # except ValueError:
        timestamp_from_kibana = raw_ts[:19]  # fallback

        # Combine DI and timestamp as unique key
        processed_key = f"{di}_{timestamp_from_kibana}"

        # --- Check if already processed ---
        cursor.execute("SELECT 1 FROM obfourb_reverse_lookup WHERE processed_key = ?", (processed_key,))
        if cursor.fetchone():
            logger.info(f"[Row {index}] [SKIP] Already processed {processed_key}, skipping.")
            continue  # Skip already processed records

        # --- Insert key to mark as processed ---
        try:
            cursor.execute("INSERT INTO obfourb_reverse_lookup (processed_key) VALUES (?)", (processed_key,))
            conn.commit()
            logger.info(f"[Row {index}] [INFO] Inserted new processed key: {processed_key}")
        except sqlite3.IntegrityError:
            logger.info(f"[Row {index}] [WARN] Duplicate key insertion skipped: {processed_key}")
            continue

        # --- Continue with your existing processing logic ---
        logger.info(di)
        destination_otp = str(row.get("@requestData.deliveryAddress", "")).strip()
        logger.info(destination_otp)

        if not destination_otp:
            logger.info(f"[Row {index}] [WARN] No delivery method found.")
            row_data = row.to_dict()
            row_data.update({
                "Match Status": "No Delivery Method",
                "Match Type": "",
                "Match Value": "",
                "BPID": "",
                "Email": ""
            })
            unmatched_rows.append(row_data)
            continue

        if di and destination_otp and (
            destination_otp == 'gert.c@vodamail.co.za' or
            'yopmail.com' in destination_otp or
            'fastmail.com' in destination_otp or 
            '@homemail.co.za' in destination_otp
        ):
            logger.info(f"[Row {index}] [OK] destination OTP suspicious — automatically unmatched.")
            row_data = row.to_dict()
            row_data.update({
                "Match Status": "Unmatched",
                "Match Type": "Direct",
                "Match Value": destination_otp,
                "BPID": "",
                "Email": di
            })
            unmatched_rows.append(row_data)
            continue

        # ✅ Step 0: Direct match between DI and destination_otp
        if di and destination_otp and di == destination_otp:
            logger.info(f"[Row {index}] [OK] DI and destination_otp are identical — automatically matched.")
            row_data = row.to_dict()
            row_data.update({
                "Match Status": "Matched",
                "Match Type": "Direct",
                "Match Value": destination_otp,
                "BPID": "",
                "Email": ""
            })
            matched_rows.append(row_data)
            continue

        # --- Step 1: Call digital ID API ---
        api_url = f"https://sbgcorehap.standardbank.co.za/security/digitalid/internal/digital-ids?username={di}"

        email = ""
        bpid = ""

        try:
            time.sleep(0.5)
            response = requests.get(api_url, timeout=10, verify=False)

            if response.status_code == 200:
                data = response.json()
                email = data.get("email", "")
                bpid = data.get("bpId", "")
                logger.info(f"[Row {index}] BPID from API: {bpid}")
            else:
                logger.info(f"[Row {index}] [ERROR] Digital ID API failed with status {response.status_code}")
                row_data = row.to_dict()
                row_data.update({
                    "Match Status": "Digital ID API Failed",
                    "Match Type": "",
                    "Match Value": "",
                    "BPID": "",
                    "Email": ""
                })
                exception_rows.append(row_data)
                continue

        except Exception as e:
            logger.info(f"[Row {index}] [ERROR] Error calling Digital ID API: {e}")
            row_data = row.to_dict()
            row_data.update({
                "Match Status": "Digital ID API Error",
                "Match Type": "",
                "Match Value": "",
                "BPID": "",
                "Email": ""
            })
            exception_rows.append(row_data)
            continue

        # --- Step 2: Check if it's a 10-digit number ---
        if destination_otp.isdigit() and len(destination_otp) == 10:
            logger.info(f"[Row {index}] [INFO] 10-digit number found — calling contact details API using BPID {bpid}.")
            if not bpid:
                logger.info(f"[Row {index}] [WARN] No BPID found to query contact details.")
                row_data = row.to_dict()
                row_data.update({
                    "Match Status": "No BPID Found",
                    "Match Type": "",
                    "Match Value": "",
                    "BPID": "",
                    "Email": email
                })
                unmatched_rows.append(row_data)
                continue

            contact_api_url = f"https://psdc-pa002tofv.za.sbicdirectory.com:7443/customer-contact-details/{bpid}"

            try:
                time.sleep(0.5)
                contact_response = requests.get(contact_api_url, timeout=10, verify=False)
                if contact_response.status_code == 200:
                    contact_data = contact_response.json()
                    contact_numbers = contact_data.get("contact_numbers", [])
                    if not contact_numbers:
                        logger.info(f"[Row {index}] [WARN] No contact numbers returned for BPID {bpid}.")
                        row_data = row.to_dict()
                        row_data.update({
                            "Match Status": "No Contact Numbers",
                            "Match Type": "",
                            "Match Value": "",
                            "BPID": bpid,
                            "Email": email
                        })
                        unmatched_rows.append(row_data)
                        continue

                    match_found = False
                    for contact in contact_numbers:
                        phone_value = str(contact.get("Phone", "")).strip()
                        if phone_value.endswith(destination_otp):
                            logger.info(f"[Row {index}] [OK] Match found! OTP: {destination_otp} == Phone: {phone_value}")
                            row_data = row.to_dict()
                            row_data.update({
                                "Match Status": "Matched",
                                "Match Type": "Phone",
                                "Match Value": phone_value,
                                "BPID": bpid,
                                "Email": email
                            })
                            matched_rows.append(row_data)
                            match_found = True
                            break

                    if not match_found:
                        logger.info(f"[Row {index}] [ERROR] No matching phone number found for OTP: {destination_otp}")
                        row_data = row.to_dict()
                        row_data.update({
                            "Match Status": "Unmatched",
                            "Match Type": "Phone",
                            "Match Value": "",
                            "BPID": bpid,
                            "Email": email
                        })
                        unmatched_rows.append(row_data)
                else:
                    logger.info(f"[Row {index}] [ERROR] Contact API failed with status {contact_response.status_code}")
                    row_data = row.to_dict()
                    row_data.update({
                        "Match Status": "Contact API Failed",
                        "Match Type": "",
                        "Match Value": "",
                        "BPID": bpid,
                        "Email": email
                    })
                    exception_rows.append(row_data)
            except Exception as e:
                logger.info(f"[Row {index}] [ERROR] Error calling Contact Details API: {e}")
                row_data = row.to_dict()
                row_data.update({
                    "Match Status": "Contact API Error",
                    "Match Type": "",
                    "Match Value": "",
                    "BPID": bpid,
                    "Email": email
                })
                exception_rows.append(row_data)

        elif not destination_otp.isdigit():
            logger.info(f"[Row {index}] [INFO] Email detected ({destination_otp}).")
            if destination_otp.lower() == email.lower():
                logger.info(f"[Row {index}] [OK] Email match found: {destination_otp} == {email}")
                row_data = row.to_dict()
                row_data.update({
                    "Match Status": "Matched",
                    "Match Type": "Email",
                    "Match Value": email,
                    "BPID": bpid,
                    "Email": email
                })
                matched_rows.append(row_data)
            else:
                logger.info(f"[Row {index}] [ERROR] Email mismatch: {destination_otp} != {email}")
                row_data = row.to_dict()
                row_data.update({
                    "Match Status": "Unmatched",
                    "Match Type": "Email",
                    "Match Value": email,
                    "BPID": bpid,
                    "Email": email
                })
                unmatched_rows.append(row_data)
        else:
            logger.info(f"[Row {index}] [WARN] Number with {len(destination_otp)} digits — possibly invalid.")
            row_data = row.to_dict()
            row_data.update({
                "Match Status": "Invalid Number",
                "Match Type": "Phone",
                "Match Value": "",
                "BPID": bpid,
                "Email": email
            })
            exception_rows.append(row_data)

    # --- Save results ---
    if matched_rows:
        pd.DataFrame(matched_rows).to_excel(matched_path, index=False)
        logger.info(f"[INFO] Saved {len(matched_rows)} matched records to {matched_path}")
    if unmatched_rows:
        pd.DataFrame(unmatched_rows).to_excel(unmatched_path, index=False)
        logger.info(f"[INFO] Saved {len(unmatched_rows)} unmatched records to {unmatched_path}")
    if exception_rows:
        pd.DataFrame(exception_rows).to_excel(exceptions_path, index=False)
        logger.info(f"[INFO] Saved {len(exception_rows)} exception records to {exceptions_path}")

    # --- Cleanup ---
    try:
        os.remove(csv_path)
        logger.info("File successfully deleted")
    except Exception as e:
        logger.info(f"[ERROR] Failed to delete file: {e}")

    conn.close()
    if unmatched_rows:
        return matched_path, unmatched_path, exceptions_path
    else:
        return False
