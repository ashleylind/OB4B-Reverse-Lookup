import pymssql
import sqlite3
import re
from datetime import datetime
import json

def extract_pended_and_write_to_sql(logger):

    def get_combined_data(logger):
        """
        Connects to MSSQL, executes a join between TFalerts Worked and TFalerts Main,
        returning all relevant fields from both tables.
        """
        try:
            with open('config/config.json') as config_file:
                config = json.load(config_file)

            last_extracted_file = config['last_extracted_filename']
            server = config['FIS_server']
            database = config['FLS_database']
            username = config['SA_user']
            password = config['SA_password']

            # Load last extracted time or default
            try:
                with open(last_extracted_file, 'r') as file:
                    last_time_str = file.read().strip()
                    last_extracted_time = datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
            except FileNotFoundError:
                last_extracted_time = datetime(2023, 8, 21)

            domain = 'SBICZA01'
            username_for_db = f"{domain}\\{username}"

            # Connect to MSSQL
            try:
                connection = pymssql.connect(server=server, port='50001', user=username_for_db, password=password, database=database)
                cursor = connection.cursor(as_dict=True)
            except Exception as e:
                logger.error(f"Error connecting to FLS database: {str(e)}")
                return []

            # Combined SQL query
            try:
                query = f"""
                WITH WorkedData AS (
                    SELECT 
                        w.*, 
                        ROW_NUMBER() OVER(PARTITION BY w.ID ORDER BY w.Insert_Date DESC) AS rn
                    FROM [Fraud_Lead_System].[dbo].[TFalerts Worked] w
                    WHERE 
                                        (w.PendedBy LIKE '%A225814' OR 
                        w.PendedBy LIKE '%a215847' OR 
                        w.PendedBy LIKE '%a217309' OR 
                        w.PendedBy LIKE '%a230490' OR 
                        w.PendedBy LIKE '%a192217' OR 
                        w.PendedBy LIKE '%a226049' OR 
                        w.PendedBy LIKE '%A182282' OR 
                        w.PendedBy LIKE '%a227314' OR 
                        w.PendedBy LIKE '%A198288' OR 
                        w.PendedBy LIKE '%A254939' OR 
                        w.PendedBy LIKE '%A214639')
                    AND w.Alert_Type = 'Online'
                    AND w.Insert_Date >= '{last_extracted_time}'
                ),
                MainData AS (
                    SELECT 
                        m.*, 
                        ROW_NUMBER() OVER(PARTITION BY m.ID ORDER BY m.SEQ) AS rn
                    FROM [Fraud_Lead_System].[dbo].[TFalerts Main] m
                )
                SELECT 
                    -- Worked fields (first per ID)
                    w.ID AS Worked_ID,
                    w.Status, w.Sub_Level_Status, w.PendedBy, w.PendStatusDate,
                    w.CompleteBy, w.CompleteDate, w.Comments, w.UpdatedInScreen,
                    w.ConfirmedFraud, w.FrustratedFraud, w.FraudType, w.Insert_Date,
                    w.TFWorkedID, w.Customer_BPID AS Worked_Customer_BPID,
                    w.Alert_Type AS Worked_Alert_Type,
                    -- Main fields (first per ID)
                    m.SEQ, m.[Action], m.[Account Number], m.[Serial Number], m.[Last Alert],
                    m.[Product Number], m.[Product Description], m.[Opened], m.[Days Open],
                    m.[Product], m.[Product Code], m.[Account Status], m.[BRI],
                    m.[Account Name], m.[Identity Info], m.[Preferred IBT], m.[Market Segment],
                    m.[Date Last CR], m.[Date Last DR], m.[Rule Number], m.[Rule Description],
                    m.[Day], m.[Time], m.[Transaction Branch], m.[DR], m.[Statement Code],
                    m.[Statement Code Description], m.[Narrative], m.[Amount],
                    m.[Transaction Status Code], m.[Telephone Number 01],
                    m.[Telephone Number 02], m.[Telephone Number 03],
                    m.[Customer Contacted], m.[Transaction Fradulent], m.[Loss Amount],
                    m.[Recovered Amount], m.[Time Stamp], m.[BlockedYN], m.[WealthToWorkYN],
                    m.[CardNumber], m.[Queue_Priority], m.[TFalertsID], m.[Dialer_Priority],
                    m.[Customer_BPID] AS Main_Customer_BPID, m.[DIgital_ID],
                    m.[Email_Address], m.[StatusCode], m.[SilentYN], m.[Alert_Type] AS Main_Alert_Type,
                    m.[Business_Unit], m.[Additional_Account_Number],
                    m.[Additional_Card_Number], m.[Customer_UUID]
                FROM WorkedData w
                LEFT JOIN MainData m ON w.ID = m.ID AND m.rn = 1
                WHERE w.rn = 1
                """

                cursor.execute(query)
                results = cursor.fetchall()
                logger.info(f"Query successful — fetched {len(results)} combined records.")
            except Exception as e:
                logger.error(f"Error executing query: {str(e)}")
                results = []
            finally:
                try:
                    cursor.close()
                    connection.close()
                except:
                    logger.warning("Error closing MSSQL connection.")

            # Update extraction timestamp
            with open(last_extracted_file, 'w') as file:
                file.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            return results

        except Exception as e:
            logger.error(f"Error in get_combined_data: {str(e)}")
            return []


    def sanitize_column_name(col):
        """Convert MSSQL column names to safe SQLite-compatible identifiers."""
        col = re.sub(r'\W+', '_', col)
        if col[0].isdigit():
            col = '_' + col
        return col


    def write_to_sqlite(data, logger):
        """
        Saves combined MSSQL data into SQLite with full schema and adds
        placeholder columns for future enrichment.
        """
        try:
            if not data:
                logger.warning("No data to write to SQLite.")
                return

            sqlite_conn = sqlite3.connect('digital_pended_alerts.db')
            cursor = sqlite_conn.cursor()

            # Get safe column names from first row
            first_row = data[0]
            safe_columns = [sanitize_column_name(c) for c in first_row.keys()]

            # Add new empty columns
            extra_columns = [
                "Username_from_staff_web",
                "ping_id_found",
                "slam_last_activate",
                "slam_last_deactivate",
                "slam_raw",
                "insert_date_of_automation"
            ]

            all_columns = safe_columns + extra_columns

            # Create table dynamically
            col_defs = ", ".join([f'"{col}" TEXT' for col in all_columns])
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS digital_pended_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {col_defs}
                )
            """)

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            for row in data:
                # Sanitize keys and values
                safe_row = {sanitize_column_name(k): (str(v) if v is not None else None) for k, v in row.items()}

                # Add empty columns
                safe_row["Username_from_staff_web"] = ''
                safe_row["ping_id_found"] = ''
                safe_row["slam_last_activate"] = ''
                safe_row["slam_last_deactivate"] = ''
                safe_row["slam_raw"] = ''
                safe_row["insert_date_of_automation"] = now

                cols = ", ".join([f'"{c}"' for c in safe_row.keys()])
                placeholders = ", ".join(["?" for _ in safe_row])
                values = list(safe_row.values())

                cursor.execute(f"INSERT INTO digital_pended_alerts ({cols}) VALUES ({placeholders})", values)

            sqlite_conn.commit()
            sqlite_conn.close()
            logger.info(f"✅ Successfully wrote {len(data)} records to digital_pended_alerts.db with new columns.")

        except Exception as e:
            logger.error(f"Error writing to SQLite: {str(e)}")


    combined_data = get_combined_data(logger)
    write_to_sqlite(combined_data, logger)