

class Login:
    """
    Class to store all xpaths for login page
    """

    USERNAME = "/html/body/div[1]/div[2]/div/form/div[1]/input"
    PASSWORD = "/html/body/div[1]/div[2]/div/form/div[2]/input"
    LOGIN_BUTTON = "/html/body/div[1]/div[2]/div/form/div[3]/a"
    


class Home:
    """
    Class to store all xpaths for home page
    """

    LOGOUT_BUTTON = "/html/body/div[20]/div[2]/form/div/span/a"
    

class Navigation:
    CASES = "pages/module/ModuleListView.jsf?page=ic:cases"
    ALERTS = "pages/module/ModuleListView.jsf?page=ic:alerts"
    REPROT_MANAGER = "pages/reports/ReportList.jsf"
    DASHBOARD = "/pages/dashboards/Dashboard.jsf"

class NewCase:
    ADD = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[2]/div/div[1]/table/tbody/tr/td/div/div/div/table/tbody/tr/td[3]/a"
    TRANSACTIONAL_FRAUD = "/html/body/div[22]/div[2]/form/span[1]/div/div/table/tbody/tr/td[1]/table/tbody/tr[6]/td[2]/span/span/input"

    NEXT_BTN = "/html/body/div[22]/div[2]/form/span[1]/table/tbody/tr/td[2]/button"


class Case:
    FILTER_FIELD = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[3]/select"
    FILTER_OPERATOR = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[4]/select"
    FILTER_VALUE_INPUT = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[5]/table/tbody/tr/td/div/table/tbody/tr/td/span/span[1]/input"
    FILTER_VALUE_DROPDOWN = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[5]/table/tbody/tr/td/div/table/tbody/tr/td/span/span[1]/select"

class OpenCase:
    """
    Class to store all xpaths for open case page
    """

    EXPORT_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td[3]/table/tbody/tr/td/span/img[1]"
    VIEW_HISTORY = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td[2]/a/img"
    ACTIONS = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td[4]/table/tbody/tr/td/span"
    ACCEPT_ACTION = "/html/body/div[16]/div[3]/div/button[2]"

class EditCase:
    EDIT_CASE_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[1]/table/tbody/tr/td/a/img"
    EDIT_CASE_SAVE_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[1]/table/tbody/tr/td[1]/a"
    EDIT_CASE_CANCEL_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/a"


class EditAccount:
    EDIT_ACCOUNT_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[1]/table/tbody/tr/td/a/img"
    EDIT_ACCOUNT_SAVE_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[1]/table/tbody/tr/td[1]/a"
    EDIT_ACCOUNT_CANCEL_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/a"

class Search:
    DROPDOWN = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[3]/select"
    CASE_NUMBER = "Case #"
    CASE_NUMBER_INPUT = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[5]/table/tbody/tr/td/div/table/tbody/tr/td/span/span[1]/input"
    CARD_NUMBER = "Fraud Card Number"
    CARD_NUMBER_INPUT = ""
    ACCOUNT_NUMBER = "Fraud Account Number"
    ACCOUNT_NUMBER_INPUT = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[2]/div/div[2]/div[1]/div/table[2]/tbody/tr[2]/td[5]/table/tbody/tr/td/div/table/tbody/tr/td/span/span[1]/input"
    SEARCH_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[2]/div/div[1]/table/tbody/tr/td/div/div/div/table/tbody/tr/td[2]/a"
    SEARCH_RESULTS_ROW1  = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[2]/div/div[2]/div[3]/table[2]/tbody/tr[2]"
    SEARCH_RESULTS_TABLE = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[2]/div/div[2]/div[3]/table[2]/tbody"


class Alert:
    pass


class Report:
    pass


class Dashboard:
    pass


class Loading:
    loadingSpinnerXpath = "/html/body/div[1]/table/tbody/tr[4]/td/form/span[1]"
    LOADING_SPINNER_ID = "statusIndicator::busy"
    

class TransactionHistory:
    TRANSACTION_TABLE = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[3]/div[2]/span/div[1]/div/div[2]/div[1]/table[2]"
    ADD_NEW_TRANSACTION = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[3]/div[2]/span/div[1]/div/div[1]/table/tbody/tr/td/div/div/div[2]/div[2]/div/table/tbody/tr/td[2]/div/div/table/tbody/tr/td[2]/a"


class TransactionEdit:
    EDIT_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[1]/table/tbody/tr/td/a/img"
    NEW_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td[2]/a/img"
    VIEW_HISTORY = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td[3]/a/img"
    EXPORT_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td[4]/table/tbody/tr/td/span/img[1]"
    

class DisplayTransactions:
    DISPLAY_TRANSACTIONS_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td[4]/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td[2]/a"
    ATTACH_BUTTON = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td/div[2]/button[1]"
    PAGES = "/html/body/div[1]/table/tbody/tr[4]/td/form/table/tbody/tr/td/div[2]/div/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr/td[3]/select"

