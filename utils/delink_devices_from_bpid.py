import pandas as pd
from staff_assist_framework.staff_assist import STAFF_ASSIST
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import os

def delink_from_bpids(logger):
    # File paths
    excel_path = r"C:\Users\C900801\OneDrive - Standard Bank\Documents\dis_to_delink_bpids.xlsx"
    dis_delinked_path = r"C:\Users\C900801\OneDrive - Standard Bank\Documents\dis_delinked.xlsx"

    # Read source Excel
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Read or create dis_delinked Excel
    if os.path.exists(dis_delinked_path):
        dis_delinked_df = pd.read_excel(dis_delinked_path)
    else:
        dis_delinked_df = pd.DataFrame(columns=["BPID", "Usernames", "Ping ID"])

    # Staff Assist setup
    staff_assist_url = 'https://staffweb.standardbank.co.za/staff-web/home'
    digital_id_input_xpath = '/html/body/div/div[2]/div[2]/div/div[2]/div/div/div[2]/label/span/input'
    ping_url = 'https://enterprisests.standardbank.co.za/delegator/#/search/users'
    toggle_block_xpath = '/html/body/div/div[2]/div[2]/div/div[3]/div/div[1]/span/div/div/div'
    select_personal_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/toolbar-component/search-component/search-filter-toggle/div/mat-button-toggle-group/mat-button-toggle[1]/button/span'
    select_bpid_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/toolbar-component/search-component/search-filter-toggle/div/mat-button-toggle-group/mat-button-toggle[3]/button/span'
    input_path_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/toolbar-component/search-component/div/mat-form-field/div/div[1]/div[2]/input'
    search_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/toolbar-component/search-component/div/mat-form-field/div/div[1]/div[3]/button/span[1]'
    customer_not_available_xpath = '/html/body/div[3]/div[2]/div/mat-dialog-container/customer-authentication/div[3]/div[3]/a'
    more_info_on_di_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/div/div/customer-details/div[2]/div/mat-card/mat-card-content/human-icon-tab-group/mat-tab-group/div/mat-tab-body[1]/div/banking-card/mat-tab-group/div/mat-tab-body[1]/div/div[1]/sbg-loading-container/div/div/div/div/div'
    username_xpath = '/html/body/staff-web/staff-pages/layout-component/mat-sidenav-container/mat-sidenav-content/div/div/customer-component/div/di-management/div/div/div/di-management-card/div/div[2]/mat-card/div/div[2]/div/section/di-common/section/section[1]/section[1]/div[2]'
    ping_search_xpath = '/html/body/div/div[2]/div[2]/div/div[2]/div/div/div[2]/label/span/input'
    collapse_result_xpath = '/html/body/div/div[2]/div[2]/div/div[3]/div/div[3]/button'
    digital_id_xpath = '/html/body/div/div[2]/div[2]/div/div[3]/div/div[3]/div/div[2]/div/div/div[2]'
    manage_ping_id_xpath = '/html/body/div/div[1]/div/div[2]/div[1]/div[2]/ul/li[1]/a'
    ping_id_input_xpath = '/html/body/div/div[2]/div[2]/div/div[2]/div/div/div/label/span/input'
    collapse_ping_id_result_xpath = '/html/body/div/div[2]/div[2]/div/div[3]/div/div[2]/button'
    delete_ping_id_xpath = '/html/body/div/div[2]/div[2]/div/div[3]/div/div[3]/span/a/button'
    delete_confirm_xpath = '/html/body/div[2]/div/div[1]/div[2]/div/div/button[2]/span'

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

    print("We have clicked edit digital id")
    time.sleep(5)

    # Loop through Excel rows
    for index, row in tqdm(df.iterrows(), total=len(df)):
        try:
            driver.driver.get(staff_assist_url)
            bpids = str(row['BP_Id'])
            wait_and_click(select_personal_xpath)
            wait_and_click(select_bpid_xpath)
            wait_and_send_keys(bpids, input_path_xpath)
            wait_and_click(search_xpath)
            try:
                wait_and_click(customer_not_available_xpath)
                wait_and_click(more_info_on_di_xpath)
                customer_found = True
            except:
                customer_found = False
                df = df[df['BP_Id'] != row['BP_Id']]
                df.to_excel(excel_path, index=False)
            if customer_found:
                try:
                    digital_id = wait_and_get_element(username_xpath)
                    dig_id_found = True
                except:
                    dig_id_found = False
                    df = df[df['BP_Id'] != row['BP_Id']]
                    df.to_excel(excel_path, index=False)
                if dig_id_found:
                    
                    
                    driver.driver.get(ping_url)
                    wait_and_send_keys(str(digital_id), ping_search_xpath)
                    wait_and_send_keys(Keys.RETURN, ping_search_xpath)
                    try:
                        wait_and_click(collapse_result_xpath)
                        di = wait_and_get_element(digital_id_xpath)
                        di_found = True
                    except:
                        di_found = False
                        df = df[df['BP_Id'] != row['BP_Id']]
                        df.to_excel(excel_path, index=False)
                    if di_found:
                        wait_and_click(manage_ping_id_xpath)
                        wait_and_send_keys(str(di), ping_id_input_xpath)
                        wait_and_send_keys(Keys.RETURN, ping_id_input_xpath)
                        max_devices = 5  # Maximum number of devices to check
                        device_index = 1
                        more_devices_found = True

                        while more_devices_found and device_index <= max_devices:
                            try:
                                # Dynamically build the XPaths for the current device
                                collapse_xpath = f"/html/body/div/div[2]/div[2]/div/div[3]/div[{device_index}]/div[2]/button"
                                delete_xpath = f"/html/body/div/div[2]/div[2]/div/div[3]/div[{device_index}]/div[3]/span/a/button"

                                # Try to collapse this ping ID result
                                wait_and_click(collapse_xpath)
                                ping_id_found = True

                            except Exception as e:
                                print(f"[INFO] No more devices found after index {device_index - 1} or collapse failed: {e}")
                                ping_id_found = False
                                df = df[df['BP_Id'] != row['BP_Id']]
                                df.to_excel(excel_path, index=False)
                                more_devices_found = False
                                break

                            if ping_id_found:
                                try:
                                    # Click the delete button and confirm
                                    wait_and_click(delete_xpath)
                                    wait_and_click(delete_confirm_xpath)

                                    print(f"[SUCCESS] Deleted device #{device_index} for BPID: {bpids}")

                                    # ✅ Update dis_delinked Excel
                                    new_row = pd.DataFrame([[bpids, digital_id, di]], columns=["BPID", "Usernames", "Ping ID"])
                                    dis_delinked_df = pd.concat([dis_delinked_df, new_row], ignore_index=True)
                                    dis_delinked_df.to_excel(dis_delinked_path, index=False)

                                    # ✅ Remove processed BPID from original Excel
                                    df = df[df['BP_Id'] != row['BP_Id']]
                                    df.to_excel(excel_path, index=False)

                                except Exception as e:
                                    print(f"[ERROR] Could not delete device #{device_index}: {e}")
                                    # If delete fails, continue to next possible device instead of breaking
                                    pass

                            # Move to next device index
                            device_index += 1

                        # Once done, mark that there are no more devices
                        more_devices_found = False
                        print(f"[DONE] Finished checking up to {device_index - 1} devices for BPID {bpids}")
        except Exception as e:
            print(f"Error processing BPID {row['BP_Id']}: {e}")
            
