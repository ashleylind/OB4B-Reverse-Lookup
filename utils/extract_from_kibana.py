import sqlite3
import pandas as pd
from elastic_framework.elastic import ELASTIC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from utils.get_login_details import get_login_details_kibana





def extract_from_kibana(logger):

    # Get all table names


# Close the connection

    kibana = 'https://melk-prod.standardbank.co.za/s/sbg_mobile/app/discover#/view/4b51ab70-2bd4-11f0-9489-8bd094f9b839?_g=h@e70a53f&_a=h@a7940f4'
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
    share_kibana_xpath = '/html/body/div[1]/header/div/div[2]/div[3]/div/div/span/nav/div/span[4]/button'
    export_share_xpath = '/html/body/div[8]/div[2]/div/div[2]/div/div[1]/button[2]/span'
    generate_csv_kibana_xpath = '/html/body/div[8]/div[2]/div/div[2]/div/div[4]/button/span'
    confirm_download_report_xpath = '/html/body/div[2]/div/div/div/div[2]/div/a/span'

    driver = ELASTIC(kibana)


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
    driver.driver.get(kibana)
    time.sleep(5)
    wait_and_click(share_kibana_xpath)
    time.sleep(5)
    try:
        wait_and_click(export_share_xpath)
    except:
        time.sleep(2)
        wait_and_click(export_share_xpath)
    time.sleep(5)
    wait_and_click(generate_csv_kibana_xpath)
    time.sleep(5)

    driver._wait_for_element_to_be_clickable(By.XPATH, confirm_download_report_xpath, timeout=360)
    driver.click_element_by_xpath(confirm_download_report_xpath)
    time.sleep(10)
    logger.info("Kibana OTP Change logs successfully extracted")



    