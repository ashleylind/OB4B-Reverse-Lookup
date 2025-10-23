import sqlite3
import pandas as pd
import requests
import re
import time

def ping_ids(logger=None):
    db_path = r'C:\Users\C900801\OneDrive - Standard Bank\Documents\Online_Alerts_Active_Deactive_Report\digital_pended_alerts.db'

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        query = """
        SELECT * FROM digital_pended_alerts
        WHERE (Username_from_staff_web != "" 
               AND Username_from_staff_web != "No username found"
               AND Username_from_staff_web IS NOT NULL)
               AND (ping_id_found != "NO PING ID FOUND")
        """
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"Error querying table: {e}")
        conn.close()
        return

    # Iterate over each record
    for index, row in df.iterrows():
        ID = row['Worked_ID']
        email_username = row['Username_from_staff_web']

        print(f"Pinging ID {ID} -> {email_username}")

        # Build API URL
        api_url = f"https://sbgcorehap.standardbank.co.za/security/digitalid/internal/digital-ids?username={email_username}"

        try:
            time.sleep(2)
            response = requests.get(api_url, timeout=10, verify=False)

            if response.status_code == 200:
                data = response.json()

                distinguished_name = data.get("distinguishedName", "")
                # Extract UUID using regex
                match = re.search(r"entryUUID=([0-9a-fA-F-]+)", distinguished_name)
                if match:
                    uuid = match.group(1)
                    print(f"→ Found UUID: {uuid}")

                    # Update database
                    cursor.execute("""
                        UPDATE digital_pended_alerts
                        SET ping_id_found = ?
                        WHERE Worked_ID = ?
                    """, (uuid, ID))
                    conn.commit()
                else:
                    print(f"⚠️ No UUID found for {email_username}")
                    cursor.execute(f"""
                        UPDATE digital_pended_alerts
                        SET ping_id_found = 'No PING ID FOUND'
                        WHERE Worked_ID = '{ID}'
                    """)
                    conn.commit()
            else:
                print(f"❌ API call failed for {email_username}, Status: {response.status_code}")
                cursor.execute(f"""
                        UPDATE digital_pended_alerts
                        SET ping_id_found = 'NO PING ID FOUND'
                        WHERE Worked_ID = '{ID}'
                    """)
                conn.commit()

        except requests.exceptions.RequestException as e:
            print(f"Error calling API for {email_username}: {e}")

    # Close DB connection
    conn.close()
    print("✅ Done processing all IDs.")
