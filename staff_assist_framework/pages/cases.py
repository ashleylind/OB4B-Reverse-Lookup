from staff_assist_framework.pages.constants import CaseActionConstants, CaseConstants, TabConstants, SystemConstants, Selection
from robot_driver_wrapper.robot_driver import By, Select, BeautifulSoup, pd
from staff_assist_framework.xpaths import xpaths
import time

class DriverAttributes:
    def __init__(self, cases) -> None:
        try:
            self.driver = cases.driver
            self._wait_timeout = cases._wait_timeout

        except:
            self.driver = cases.driver
            self._wait_timeout = cases.wait_timeout

        for attribute in [
            '_wait_for_element',
            '_wait_for_element_to_be_clickable',
            '_wait_for_element_to_be_invisible',
            '_wait_for_element_to_be_visible',
            '_wait_for_loading',
            'wait_for_iecm_spinner',
            '_wait_for_elements',
        ]:
            setattr(self, attribute, getattr(cases, attribute))
    
class Shared(DriverAttributes):

    def __init__(self, iecm) -> None:
        super().__init__(iecm)


    def set_field_value(self, field: CaseConstants, value: str, section: int=-1, select_by=Selection.VISIBLE_TEXT, side: str = "left", has_spinner: bool = False, fuzzy: bool = False):
        
        
        if fuzzy:
            ele = self._wait_for_elements(
            By.XPATH, f'//*[contains(text(),"{field}")]')[section]
        else:
            ele = self._wait_for_elements(
            By.XPATH, f'//*[text()="{field}"]')[section]

        if side == "left":
            current_ele = ele.find_element(By.XPATH, "../../td[2]")
        else:
            current_ele = ele.find_element(By.XPATH, "../../td[4]")

        is_select = True if len(current_ele.find_elements(
            By.TAG_NAME, 'select')) > 0 else False
        is_textarea = True if len(current_ele.find_elements(
            By.TAG_NAME, 'textarea')) > 0 else False

        if is_select:
            select = Select(current_ele.find_elements(
                By.TAG_NAME, 'select')[-1])
            if select_by == Selection.VALUE:
                select.select_by_value(value)
            elif select_by == Selection.INDEX:
                select.select_by_index(value)
            elif select_by == Selection.VISIBLE_TEXT:
                select.select_by_visible_text(value)
                
            if has_spinner:
                self.wait_for_iecm_spinner()
        elif is_textarea:
            print("textarea")
            current_ele.find_elements(
                By.TAG_NAME, 'textarea')[-1].send_keys(value)
        
        else:
            is_checkbox = True if current_ele.find_elements(By.TAG_NAME, 'input')[-1].get_attribute('type') == 'checkbox' else False
            if is_checkbox:
                if current_ele.find_elements(By.TAG_NAME, 'input')[-1].is_selected():
                    pass
                else:
                    current_ele.find_elements(By.TAG_NAME, 'input')[-1].click()
            else:
                current_ele.find_elements(
                    By.TAG_NAME, 'input')[-1].clear()
                current_ele.find_elements(
                    By.TAG_NAME, 'input')[-1].send_keys(value)


    def cancel(self):
        try:
            ele = self._wait_for_element(
                By.XPATH, xpaths.EditCase.EDIT_CASE_SAVE_BUTTON, 10)
            self.driver.execute_script(ele.get_attribute("onclick"))
            self.wait_for_iecm_spinner()

        except Exception as e:
            ele = self._wait_for_element(
                By.LINK_TEXT, 'Cancel', 10)
            self.driver.execute_script(ele.get_attribute("onclick"))


    def save(self):
        try:
            ele = self._wait_for_element(
                By.XPATH, xpaths.EditCase.EDIT_CASE_SAVE_BUTTON, 10)
            self.driver.execute_script(ele.get_attribute("onclick"))
            self.wait_for_iecm_spinner()

        except Exception as e:
            ele = self._wait_for_element(
                By.LINK_TEXT, 'Save', 10)
            self.driver.execute_script(ele.get_attribute("onclick"))



class DisplayTransactions(DriverAttributes):

    def __init__(self, cases) -> None:
        super().__init__(cases)


    def get_transaction_count(self):
        return len(self._wait_for_elements(By.XPATH, xpaths.DisplayTransactions.TRANSACTION_COUNT))


    def get_transactions_table(self):
        try:
            current_ele = Select(self._wait_for_element(By.XPATH, xpaths.DisplayTransactions.PAGES))
            current_ele.select_by_value("all")
            time.sleep(3)
        except:
            pass

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        data = []
        table = soup.find('table', attrs={'class': 'af_table_content'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('th')
            header = [ele.text.strip() for ele in cols]
            break

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            if len(cols) == 10:
                data.append(cols)

        return pd.DataFrame.from_records(data, columns=header)


    def select_transaction(self, transaction_id: str):
        ele = self._wait_for_element(By.XPATH, f'//*[text()="{transaction_id}"]')
        ele.find_element(By.XPATH, "../td").find_elements(By.TAG_NAME, 'input')[-1].click()


    def attach(self):
        ele = self._wait_for_element(By.XPATH, xpaths.DisplayTransactions.ATTACH_BUTTON)
        self.driver.execute_script(ele.get_attribute("onclick"))
        self.wait_for_iecm_spinner()


class Search(DriverAttributes):

    def __init__(self, cases) -> None:
        super().__init__(cases)

    # TODO: Add more search options

    def by(self, field, opertaor, value):
        pass

    def case_number(self, case_number, has_spinner=True) -> bool:
        select = Select(self._wait_for_element(
            By.XPATH, xpaths.Search.DROPDOWN, 10))
        select.select_by_visible_text(xpaths.Search.CASE_NUMBER)
        if has_spinner:
            self.wait_for_iecm_spinner()
            self._wait_for_element(
            By.XPATH, xpaths.Search.CASE_NUMBER_INPUT, 10).clear()
        self._wait_for_element(
            By.XPATH, xpaths.Search.CASE_NUMBER_INPUT, 10).send_keys(case_number)
        self._wait_for_element_to_be_clickable(By.XPATH, xpaths.Search.SEARCH_BUTTON, 10).click()
        self.wait_for_iecm_spinner()

        return "No records were found." not in self.driver.page_source

    def card_number(self, card_number) -> bool:
        select = Select(self._wait_for_element(
            By.XPATH, xpaths.Search.DROPDOWN, 10))
        select.select_by_visible_text(xpaths.Search.CARD_NUMBER)
        self.wait_for_iecm_spinner()
        self._wait_for_element(
            By.XPATH, xpaths.Search.CASE_NUMBER_INPUT, 10).clear()
        self._wait_for_element(
            By.XPATH, xpaths.Search.CASE_NUMBER_INPUT, 10).send_keys(card_number)
        self._wait_for_element_to_be_clickable(By.XPATH, xpaths.Search.SEARCH_BUTTON, 10).click()
        self.wait_for_iecm_spinner()

        return not bool(self.driver.find_elements(By.CLASS_NAME, SystemConstants.GLOBAL_MESSAGE_ERROR))

    def account_number(self, account_number) -> bool:
        select = Select(self._wait_for_element(
            By.XPATH, xpaths.Search.DROPDOWN, 10))
        select.select_by_visible_text(xpaths.Search.ACCOUNT_NUMBER)
        self.wait_for_iecm_spinner()
        self._wait_for_element(
            By.XPATH, xpaths.Search.ACCOUNT_NUMBER_INPUT, 10).clear()
        self._wait_for_element(
            By.XPATH, xpaths.Search.ACCOUNT_NUMBER_INPUT, 10).send_keys(account_number)
        self._wait_for_element_to_be_clickable(By.XPATH, xpaths.Search.SEARCH_BUTTON, 10).click()
        self.wait_for_iecm_spinner()

        return not bool(self.driver.find_elements(By.CLASS_NAME, SystemConstants.GLOBAL_MESSAGE_ERROR))

    def get_search_results(self) -> pd.DataFrame:
        data = []
        for i, t in enumerate(self.driver.find_element(By.XPATH, xpaths.Search.SEARCH_RESULTS_TABLE).find_elements(By.TAG_NAME, 'tr')):
            line = t.text.split('\n')
            if len(line) > 1:
                if i == 0:
                    header = line
                else:
                    data.append(line)
        
        return pd.DataFrame(data, columns=header)


class CreateNew(Shared):
    def __init__(self, cases) -> None:
        super().__init__(cases)
        try:
            setattr(self, 'open_case', getattr(cases, 'open_case'))
        except AttributeError:
            pass

    def __call__(self):
        script = self.driver._wait_for_element(By.XPATH, xpaths.NewCase.ADD).get_attribute("onclick")
        self.driver.execute_script(script)
        self.wait_for_iecm_spinner()

class EditCase(Shared):

    def __init__(self, cases) -> None:
        super().__init__(cases)
        try:
            setattr(self, 'open_case', getattr(cases, 'open_case'))
        except AttributeError:
            pass

    def __call__(self, should_open=True):
        if should_open:
            self.open_case()
        self._wait_for_element_to_be_clickable(
            By.XPATH, xpaths.EditCase.EDIT_CASE_BUTTON, 10).click()
        self.wait_for_iecm_spinner()


class OpenCase(DriverAttributes):

    def __init__(self, cases) -> None:
        super().__init__(cases)

    def __call__(self) -> None:
        self._wait_for_element_to_be_clickable(
            By.XPATH, xpaths.Search.SEARCH_RESULTS_ROW1, 10).click()
        # self.wait_for_iecm_spinner()

    def get_field_value(self, field: CaseConstants, side: str = "left"):
        ele = self._wait_for_elements(
            By.XPATH, f'//*[contains(text(),"{field}")]')[-1]

        if side == "left":
            return ele.find_element(By.XPATH, "../../td[2]").text
        else:
            return ele.find_element(By.XPATH, "../../td[4]").text

    def open_case_tab(self, tab: TabConstants):
        ele = self._wait_for_elements(
            By.XPATH, f'//*[contains(text(),"{tab}")]')[-1]
        self.driver.execute_script(ele.get_attribute("onclick"))
        self.wait_for_iecm_spinner()

    def get_transaction_history(self):
        return TransactionHistory.get_transaction_history(self)


    def open_account(self, account_number):
        self._wait_for_elements(By.LINK_TEXT, account_number)[-1].click()
        return OpenAccount(self)


    def edit_account(self, account_number):
        self.open_account(account_number)
        self._wait_for_element_to_be_clickable(By.XPATH, xpaths.EditAccount.EDIT_ACCOUNT_BUTTON, 10).click()
        self.wait_for_iecm_spinner()

        return EditAccount(self)


    def display_transactions(self):
        on_click = self._wait_for_element_to_be_clickable(By.XPATH, xpaths.DisplayTransactions.DISPLAY_TRANSACTIONS_BUTTON, 10).get_attribute("onclick")
        self.driver.execute_script(on_click)
        self.wait_for_iecm_spinner()

        return DisplayTransactions(self)



    @property
    def edit(self):
        self._wait_for_element_to_be_clickable(
            By.XPATH, xpaths.EditCase.EDIT_CASE_BUTTON, 10).click()
        self.wait_for_iecm_spinner()
        return EditCase(self)


class TransactionHistory(DriverAttributes):

    def __init__(self, cases) -> None:
        super().__init__(cases)

    @staticmethod
    def get_transaction_history(self) -> pd.DataFrame:
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        data = []
        table = soup.find('table', attrs={'class': 'af_table_content'})
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if len(cols) == 26:
                data.append(cols[8:])  # Get rid of empty values

        h = self._wait_for_element(By.XPATH, xpaths.TransactionHistory.TRANSACTION_TABLE, timeout=10).find_elements(
            By.TAG_NAME, 'tr')[0].text.split('\n')
        h.append('None')
        h

        return pd.DataFrame.from_records(data, columns=h)


class Cases(DriverAttributes):

    def __init__(self, iecm) -> None:
        super().__init__(iecm)

    @property
    def search(self):
        return Search(self)

    @property
    def edit_case(self):
        return EditCase(self)

    @property
    def open_case(self):
        return OpenCase(self)


    @property
    def create_new(self):
        return CreateNew(self)

    @property
    def display_transactions(self):
        return DisplayTransactions(self)

    def open_case_by_case_number(self, case_number):
        self.case_number(case_number)
        self.open_case(self._wait_for_element(
            By.XPATH, xpaths.Search.SEARCH_RESULTS_ROW1, 10))

    def open_case_by_card_number(self, card_number):
        self.card_number(card_number)
        self.open_case(self._wait_for_element(
            By.XPATH, xpaths.Search.SEARCH_RESULTS_ROW1, 10))


class Account(DriverAttributes):
    def __init__(self, iecm) -> None:
        super().__init__(iecm)


    @property
    def edit_account(self):
        return EditAccount(self)

    @property
    def open_account(self):
        return OpenAccount(self)


class EditAccount(Shared):

    def __init__(self, cases) -> None:
        super().__init__(cases)

    def __call__(self, account_number):
        self._wait_for_elements(By.LINK_TEXT, account_number)[-1].click()
        self._wait_for_element_to_be_clickable(
            By.XPATH, xpaths.EditAccount.EDIT_ACCOUNT_BUTTON, 10).click()
        self.wait_for_iecm_spinner()


class OpenAccount(DriverAttributes):

    def __init__(self, cases) -> None:
        super().__init__(cases)

    def __call__(self, account_number) -> None:
        self._wait_for_elements(By.LINK_TEXT, account_number)[-1].click()
        # self.wait_for_iecm_spinner()

    def get_field_value(self, field: CaseConstants, side: str = "left"):
        ele = self._wait_for_elements(
            By.XPATH, f'//*[contains(text(),"{field}")]')[-1]

        if side == "left":
            return ele.find_element(By.XPATH, "../../td[2]").text
        else:
            return ele.find_element(By.XPATH, "../../td[4]").text


class Transaction(DriverAttributes):
    def __init__(self, iecm) -> None:
        super().__init__(iecm)


    @property
    def edit(self):
        return EditTransaction(self)

    @property
    def open(self):
        return OpenTransaction(self)

    @property
    def add(self):
        return AddTransaction(self)


class EditTransaction(Shared):

    def __init__(self, cases) -> None:
        super().__init__(cases)

    def __call__(self, id):
        self._wait_for_elements(By.XPATH, f'//*[contains(text(),"{id}")]')[-1].click()
        self._wait_for_element_to_be_clickable(
            By.XPATH, xpaths.EditAccount.EDIT_ACCOUNT_BUTTON, 10).click()
        self.wait_for_iecm_spinner()


class OpenTransaction(DriverAttributes):

    def __init__(self, cases) -> None:
        super().__init__(cases)

    def __call__(self, id) -> None:
        self._wait_for_elements(By.XPATH, f'//*[contains(text(),"{id}")]')[-1].click()
        # self.wait_for_iecm_spinner()

    def get_field_value(self, field: CaseConstants, side: str = "left"):
        ele = self._wait_for_elements(
            By.XPATH, f'//*[contains(text(),"{field}")]')[-1]

        if side == "left":
            return ele.find_element(By.XPATH, "../../td[2]").text
        else:
            return ele.find_element(By.XPATH, "../../td[4]").text


class AddTransaction(Shared):

    def __init__(self, cases) -> None:
        super().__init__(cases)

    def __call__(self) -> None:
        self._wait_for_elements(By.XPATH, xpaths.TransactionHistory.ADD_NEW_TRANSACTION)[-1].click()
        # self.wait_for_iecm_spinner()



class MoveCase(DriverAttributes):
    def __init__(self, cases) -> None:
        super().__init__(cases)

    def __call__(self, queue: CaseActionConstants) -> None:
        self.driver.execute_script(self._wait_for_element(By.XPATH, f'//*[contains(text(),"{queue}")]', 10).get_attribute('onclick'))
        self.wait_for_iecm_spinner()
        self._wait_for_element_to_be_clickable(By.XPATH, "/html/body/div[16]/div[3]/div/button[2]/span").click()
        self.wait_for_iecm_spinner()


class CaseActions(DriverAttributes):

    def __init__(self, iecm) -> None:
        super().__init__(iecm)

    @property
    def move_to(self):
        return MoveCase(self)


