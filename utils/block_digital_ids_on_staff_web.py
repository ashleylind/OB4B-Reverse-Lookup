import pandas as pd
from staff_assist_framework.staff_assist import STAFF_ASSIST
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
from datetime import datetime
import os
from utils.splunk_reporting import log_bot_event

def deactive_digital_ids(logger, excel_path):
    # Read the Excel file
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        logger.info(f"Error reading excel file: {e}")
        return

    # Prepare a results list
    results = []

    # Staff Assist setup
    staff_assist_url = 'https://enterprisests.standardbank.co.za/delegator/#/search/users'
    digital_id_input_xpath = '/html/body/div/div[2]/div[2]/div/div[2]/div/div/div[2]/label/span/input'

    driver = STAFF_ASSIST(staff_assist_url)

    def wait_and_click(xpath):
        driver._wait_for_element_to_be_clickable(By.XPATH, xpath, timeout=2)
        driver.click_element_by_xpath(xpath)

    def wait_and_send_keys(keys, xpath):
        driver._wait_for_element_to_be_clickable(By.XPATH, xpath, timeout=2)
        driver.send_keys_by_xpath(xpath, keys)

    def wait_and_get_element(xpath):
        driver._wait_for_element_to_be_clickable(By.XPATH, xpath, timeout=2)
        return driver.get_text_by_xpath(xpath)


    username = ''
    password = ''
    try:
        driver.login(username, password)
    except:
        time.sleep(0.1)

    logger.info("We have clicked edit digital id")

    # Loop over each row in the Excel file
    for index, row in tqdm(df.iterrows(), total=len(df)):
        start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        digital_id = str(row['@digitalId']).strip()
        otp_destination = str(row['@requestData.deliveryAddress']).strip()
        logger.info(f"Processing digital ID: {digital_id}")
        matched = False
        status = "Different OTP Destination, not in disable criteria"
        if otp_destination == 'gert.c@vodamail.co.za' or '@yopmail' in otp_destination or 'fastmail.com' in otp_destination or 'homemail.co.za' in otp_destination:
            time.sleep(5)
            wait_and_send_keys(digital_id, digital_id_input_xpath)
            wait_and_send_keys(Keys.RETURN, digital_id_input_xpath) 
            for number in range(1, 7):
                username_xpath = f'/html/body/div/div[2]/div[2]/div/div[3]/div[{number}]/div[2]/div[1]'
                toggle_xpath = f"//div[@class='input-toggle selected'][{number}]"

                try:
                    data = wait_and_get_element(username_xpath)
                    logger.info(f"Data from ping - {str(data).strip().lower()}")
                    logger.info(f"Data from kibana - {digital_id.lower()}")
                    if str(data).strip().lower() == digital_id.lower():  
                        
                        logger.info(f"[Row {index}] Match found — clicking toggle for otp dest {otp_destination}")
                        try:
                            wait_and_click(toggle_xpath)
                            status = "Disabled"
                            end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            status_splunk, text = log_bot_event(start, end, 1, str(digital_id), logger)
                            print(f"Splunk response [{status_splunk}]: {text}")



                        except:
                            try:
                                driver._wait_for_element_to_be_clickable(By.XPATH, f"//div[@class='input-toggle'][{number}]")
                                logger.info("Device already disabled")
                                status = "Already Disabled"
                            except:
                                logger.info(f"Issue with {digital_id}")
                                status = "Error"
                        matched = True
                        break
                except Exception:
                    continue

        if not matched:
            logger.info(f"[Row {index}] Unmatched OTP destination not in disable criteria {digital_id}")

        # Append to results log
        results.append({
            "Digital ID": digital_id,
            "OTP Destination": otp_destination,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Status": status
        })


    # Save the results to Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path = os.path.join(os.path.dirname(excel_path), f"Digital_ID_Disable_Report_{timestamp}.xlsx")
    pd.DataFrame(results).to_excel(output_path, index=False)
    logger.info(f"\n Results saved to: {output_path}")
    if results:
        return output_path
    else:
        return False
