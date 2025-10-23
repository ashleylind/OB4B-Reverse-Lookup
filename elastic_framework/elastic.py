from robot_driver_wrapper.robot_driver import RobotDriver, By
from elastic_framework import xpaths
from elastic_framework.pages.home import Navigate
from elastic_framework.pages.cases import CaseActions, Cases, Account, DisplayTransactions, Transaction

class PasswordIncorrectError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ELASTIC(RobotDriver):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._navigate = Navigate(self)
        self._cases = Cases(self)
        self._account = Account(self)
        self._transaction = Transaction(self)
        self._case_action = CaseActions(self)
        self._display_transactions = DisplayTransactions(self)



    def login(self, username, password):
        self.driver.get(self.system_url)
        self._wait_for_element(By.XPATH, xpaths.Login.USERNAME, 10).clear()
        self._wait_for_element(By.XPATH, xpaths.Login.USERNAME, 10).send_keys(username)
        self._wait_for_element(By.XPATH, xpaths.Login.PASSWORD, 10).clear()
        self._wait_for_element(By.XPATH, xpaths.Login.PASSWORD, 10).send_keys(password)
        self._wait_for_element(By.XPATH, xpaths.Login.LOGIN_BUTTON, 10).click()
        
        if self.driver.current_url.lower().endswith("j_security_check"):
            raise PasswordIncorrectError("IECM Credentials are incorrect")

    def logoff(self):
        self.driver.execute_script(self.driver.find_element(By.XPATH, xpaths.Home.LOGOUT_BUTTON).get_attribute('onclick'))
        self.driver.close()
        self.driver.quit()
        

    @property
    def navigate_to(self):
        return self._navigate


    @property
    def cases(self):
        return self._cases


    def wait_for_iecm_spinner(self):
        _located = False
        _count = 0
        while not _located:
            try:
                self._wait_for_element_to_be_visible(By.ID, xpaths.Loading.LOADING_SPINNER_ID, 1)
                _located = True
            except:
                _count += 1
                if _count > 10:
                    _located = True

        _located = False
        _count = 0
        while not _located:
            try:
                self._wait_for_element_to_be_invisible(By.ID, xpaths.Loading.LOADING_SPINNER_ID, 1)
                _located = True
            except:
                _count += 1
                if _count > 10:
                    _located = True

    
    @property
    def open_case(self):
        return self._cases.open_case


    @property
    def edit_case(self):
        return self._cases.edit_case


    @property
    def account(self):
        return self._account


    @property
    def transaction(self):
        return self._transaction

    @property
    def case_actions(self):
        return self._case_action

    @property
    def display_transactions(self):
        return self._display_transactions


    @property
    def create_new(self):
        return self._cases.create_new


    def bread_crum_pervious(self):
        self.driver.find_element(By.CLASS_NAME, "breadcrumbs").find_elements(By.TAG_NAME, 'a')[-1].click()

    
    def get_text_by_xpath(self, xpath):
        try:
            element = self._wait_for_element(By.XPATH, xpath, 60)
            return element.text
        except Exception as e:
            print(f"Error getting text by XPath: {str(e)}")
            return None
        
    def click_element_by_xpath(self, xpath):
        try:
            element = self._wait_for_element_to_be_clickable(By.XPATH, xpath, 10)
            element.click()
        except Exception as e:
            print(f"Error clicking element by XPath: {str(e)}")

    def click_element_by_name(self, element_name):
        try:
            element = self._wait_for_element_to_be_clickable(By.NAME, element_name, 10)
            element.click()
        except Exception as e:
            print(f"Error clicking element by name '{element_name}': {str(e)}")

    def send_keys_by_name(self, element_name, keys_to_send):
        try:
            element = self._wait_for_element(By.NAME, element_name, 10)
            element.clear()  # Clear any existing text in the input field
            element.send_keys(keys_to_send)
        except Exception as e:
            print(f"Error sending keys '{keys_to_send}' to element by name '{element_name}': {str(e)}")

    def send_keys_by_xpath(self, element_name, keys_to_send):
        try:
            element = self._wait_for_element(By.XPATH, element_name, 10)
            element.clear()  # Clear any existing text in the input field
            element.send_keys(keys_to_send)
        except Exception as e:
            print(f"Error sending keys '{keys_to_send}' to element by name '{element_name}': {str(e)}")



