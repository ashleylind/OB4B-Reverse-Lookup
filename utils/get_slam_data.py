import sqlite3
import pandas as pd
from elastic_framework.elastic import ELASTIC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from utils.get_login_details import get_login_details_kibana





def get_slam_data(logger):
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
        WHERE ping_id_found != "NO PING ID FOUND"
        AND ping_id_found != ""
        """            
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"Error querying table: {e}")

# Close the connection
    conn.close()

    slam_url = 'https://logweb.standardbank.co.za/s/it-security---test/app/r/s/VDuD6'
    ping_id_input_xpath = '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div/div/div[1]/div/textarea'
    no_data_found_xpath = '/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/h2'
    search_session_xpath = "//button[@aria-label='Search session complete']"
    select_all_results_xpath = "//input[@aria-label='Select all visible rows']"
    deselect_all_results_xpath = "//input[@aria-label='Deselect all visible rows']"
    selected_drop_down_xpath = '/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/span/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div/div'
    copy_doc_as_json_xpath = '/html/body/div[7]/div[2]/div/div[2]/div/div/button[3]/span'
    accept_ts_and_cs_xpath = '/html/body/div/div/form/input[1]'
    username_input = '/html/body/div/div/form/input[2]'
    password_input_xpath = '/html/body/div/div/form/input[3]'
    login_button_xpath = '/html/body/div/div/form/input[4]'
    username_elastic_xpath = '/html/body/div[1]/div[3]/div[2]/div/div/div/div/div/form/div[1]/div[2]/div/div/input'
    password_elastic_xpath = '/html/body/div[1]/div[3]/div[2]/div/div/div/div/div/form/div[2]/div[2]/div/div[1]/input'
    login_elastic_xpath = '/html/body/div[1]/div[3]/div[2]/div/div/div/div/div/form/div[4]/div/button/span'
    cancel_search_xpath = '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/div[3]/div/div/div/div[2]/button'
    update_and_search_xpath = '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/div[3]/div/div/div/div[2]/span/button'


    driver = ELASTIC(slam_url)


    def wait_and_click(xpath):
        driver._wait_for_element_to_be_clickable(By.XPATH, xpath, timeout=20)
        driver.click_element_by_xpath(xpath)

    def wait_and_send_keys(keys, xpath):
        driver._wait_for_element_to_be_clickable(By.XPATH, xpath, timeout=20)
        driver.send_keys_by_xpath(xpath, keys)

    def wait_and_get_element(xpath):
        driver._wait_for_element_to_be_clickable(By.XPATH, xpath, timeout=20)
        return driver.get_text_by_xpath(xpath)
    username = 'BCBFraudIECMTwoBot.IECMTwo@standardbank.co.za'
    domain, user, password = get_login_details_kibana()
    try:
        driver.login(username, password)
    except:
        time.sleep(0.1)
    wait_and_click(accept_ts_and_cs_xpath)
    wait_and_send_keys(username, username_input)
    wait_and_send_keys(password, password_input_xpath)
    wait_and_click(login_button_xpath)
    wait_and_send_keys(username, username_elastic_xpath)
    wait_and_send_keys(password, password_elastic_xpath)
    wait_and_click(login_elastic_xpath)
    time.sleep(5)
    driver.driver.get(slam_url)
    wait_and_click(cancel_search_xpath)
    time.sleep(5)

    for index, row in df.iterrows():
        ID = row['Worked_ID']
        ping_id = row['ping_id_found']
        
        wait_and_send_keys(f"\"{ping_id}\"", ping_id_input_xpath)
        wait_and_click(update_and_search_xpath)
        # driver._wait_for_element_to_be_visible(By.XPATH, search_session_xpath, timeout=240)
        time.sleep(10)
        data_found = ""
        try:
            driver._wait_for_element_to_be_visible(By.XPATH, no_data_found_xpath)
            data_found = False
        except:
            data_found = True
            driver._wait_for_element_to_be_clickable(By.XPATH, select_all_results_xpath, timeout=240)
            print("We have found data")

        if data_found:
            try:
                wait_and_click(select_all_results_xpath)
            except:
                wait_and_click(deselect_all_results_xpath)
                wait_and_click(select_all_results_xpath)
            wait_and_click(selected_drop_down_xpath)
            wait_and_click(copy_doc_as_json_xpath)




    