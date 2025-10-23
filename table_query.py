import sqlite3
import pandas as pd

# Path to your SQLite database
db_path = r'C:\Users\C900801\OneDrive - Standard Bank\Documents\Online_Alerts_Active_Deactive_Report\digital_pended_alerts.db'
target_cardholder = '5284973271857595'
target_reference = '05221005161435831005164'
taget_auth = '539615'
target_amount = '540.00'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

# Search all tables for the target Cardholder Number AND Reference Number
for table in tables:
    try:
        # query = f"""
        #     SELECT * FROM `{table}`
        #     WHERE `Cardholder Number` = ? AND `Reference Number` = ? 
        #     AND `Authorization Code` = ? AND `Transaction Amount` = ?
        # """

        # df = pd.read_sql_query(query, conn, params=(target_cardholder, target_reference, taget_auth, target_amount))
        query = f"""
                        SELECT CardNumber, Username_from_staff_web, Worked_ID, ping_id_found FROM digital_pended_alerts
            WHERE ping_id_found = ""
                
            
        """
        # cursor.execute(query)
        
        df = pd.read_sql_query(query, conn)
        for index, row in df.iterrows():
            print(row)

        # if not df.empty:
        #     print(f"\nMatches found in table: {table}")
        #     print(df.to_string(index=False))
        #     for index, row in df.iterrows():
        #         for item in row:
        #             print(item)
    except Exception as e:
        print(f"Error querying table {table}: {e}")

# Close the connection
conn.close()
