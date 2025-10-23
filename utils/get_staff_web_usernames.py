import sqlite3
import pandas as pd
from staff_assist_framework.staff_assist import STAFF_ASSIST
from selenium.webdriver.common.by import By
import time




def get_staff_assist_usernames(logger):
    db_path = r'C:\Users\C900801\OneDrive - Standard Bank\Documents\Online_Alerts_Active_Deactive_Report\digital_pended_alerts.db'
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names

    try:
        # query = f"""
        #     SELECT * FROM `{table}`
        #     WHERE `Cardholder Number` = ? AND `Reference Number` = ? 
        #     AND `Authorization Code` = ? AND `Transaction Amount` = ?
        # """

        # df = pd.read_sql_query(query, conn, params=(target_cardholder, target_reference, taget_auth, target_amount))
        query = f"""
        SELECT * FROM digital_pended_alerts
        WHERE (`CardNumber` != 'xxxxxxxxxxxxxxxx' OR `CardNumber` is not NULL)
        AND `Username_from_staff_web` = ''
            
        """            
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"Error querying table: {e}")

# Close the connection
    conn.close()

    staff_assist_url = 'https://staffweb.standardbank.co.za/staff-web/home'
    di_management_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/div/div/home-component/quick-start-container/div/div[2]/div[2]/quick-start-card'
    card_number_select_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/div/div/staff-web-di-search/div/div[2]/div[2]/mat-button-toggle-group/mat-button-toggle[2]/button/span'
    card_number_input_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/div/div/staff-web-di-search/div/div[2]/div[1]/div/input'
    username_staff_assist_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/div/div/staff-web-di-search/div/div[4]/di-search-results-card/div/div[3]'
    search_card_number_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/div/div/staff-web-di-search/div/div[2]/div[1]/div/button/span[2]'
    user_id_not_found_xpath = '/html/body/div[3]/div/div/snack-bar-container/div/div/sbg-snackbar/div[2]'
    view_card_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/div/div/staff-web-di-search/div/div[4]/di-search-results-card/div/sbg-button-container/div/sbg-button/button/span[1]/div'
    email_address_field_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/div/div/di-manage/div/div[2]/mat-card/div/div[2]/div/di-information/sbg-loading-container/div/div/div[2]'
    done_on_card_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/div/div/di-manage/div/div[2]/mat-card/div/div[2]/div/di-information/div/sbg-button-ng/button/span[1]/div'
    back_to_di_management_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/taskbar-component/sbg-taskbar/mat-toolbar/mat-toolbar-row/mat-chip-list/div/mat-basic-chip[2]/div[2]/div'


    driver = STAFF_ASSIST(staff_assist_url)


    def wait_and_click(xpath):
        driver._wait_for_element_to_be_clickable(By.XPATH, xpath, timeout=20)
        driver.click_element_by_xpath(xpath)

    def wait_and_send_keys(keys, xpath):
        driver._wait_for_element_to_be_clickable(By.XPATH, xpath, timeout=20)
        driver.send_keys_by_xpath(xpath, keys)

    def wait_and_get_element(xpath):
        driver._wait_for_element_to_be_clickable(By.XPATH, xpath, timeout=20)
        return driver.get_text_by_xpath(xpath)
    username = ''
    password = ''
    try:
        driver.login(username, password)
    except:
        time.sleep(0.1)
    wait_and_click(di_management_xpath)
    wait_and_click(card_number_select_xpath)


    for index, row in df.iterrows():
        ID = row['Worked_ID']
        card_number = row['CardNumber']
        print(card_number)
        wait_and_send_keys(str(card_number), card_number_input_xpath)
        wait_and_click(search_card_number_xpath)
        try:
            driver._wait_for_element_to_be_clickable(By.XPATH, view_card_xpath, timeout=2)
            
            driver.click_element_by_xpath(view_card_xpath)
            username_to_update = wait_and_get_element(email_address_field_xpath)
            print(username_to_update)

            lines = username_to_update.strip().splitlines()
            final_email = [line for line in lines if line.strip().lower() != "username"]
            print(str(final_email[0]))
            db_path = r'C:\Users\C900801\OneDrive - Standard Bank\Documents\Online_Alerts_Active_Deactive_Report\digital_pended_alerts.db'
            # Connect to the database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Get all table names

            try:
                query = f"""
                UPDATE digital_pended_alerts
                SET Username_from_staff_web = '{str(final_email[0])}'
                WHERE Worked_ID = '{str(ID)}'
                    
                """    
                cursor.execute(query)    
                conn.commit()
                conn.close()    
            except Exception as e:
                print(f"Error updating table digital_pended_alerts: {e}")

            wait_and_click(back_to_di_management_xpath)
            wait_and_click(card_number_select_xpath)


        except:
            try:

                no_result = wait_and_get_element(user_id_not_found_xpath)
                print(no_result)
                db_path = r'C:\Users\C900801\OneDrive - Standard Bank\Documents\Online_Alerts_Active_Deactive_Report\digital_pended_alerts.db'
                # Connect to the database
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Get all table names

                try:
                    query = f"""
                    UPDATE digital_pended_alerts
                    SET Username_from_staff_web = 'No username found'
                    WHERE Worked_ID = '{str(ID)}'
                        
                    """    
                    cursor.execute(query)    
                    conn.commit()
                    conn.close()    
                except Exception as e:
                    print(f"Error updating table digital_pended_alerts: {e}")
            except:
                print("Issue")
                wait_and_click(back_to_di_management_xpath)
                wait_and_click(card_number_select_xpath)




  







