from staff_assist_framework.xpaths import xpaths

class Navigate:
    

    def __init__(self, iecm) -> None:
        self._driver = iecm.driver
        self._system_url = iecm.system_url
        

    
    def cases(self):
        self._driver.get(self._system_url + xpaths.Navigation.CASES)


    def dashboard(self):
        self._driver.get(self._system_url + xpaths.Navigation.DASHBOARD)

    
    def alerts(self):
        self._driver.get(self._system_url + xpaths.Navigation.ALERTS)

    
    def report_manager(self):
        self._driver.get(self._system_url + xpaths.Navigation.REPORT_MANAGER)


