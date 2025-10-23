from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from .utils import get_chrome_driver, get_edge_driver
import platform
from bs4 import BeautifulSoup
import pandas as pd




class RobotDriver:
    def __init__(self, url: str, timeout: int = 5, *args, **kwargs) -> None:

        if not url:
            raise Exception("URL is required")

        self.wait_timeout = timeout
        self.system_url = url

        try:
            self._initialize_driver(*args, **kwargs)
        except WebDriverException as e:
            if platform.system() == "win32" or platform.system() == "Windows":
                self._download_edge_driver()
                self._initialize_driver(*args, **kwargs)
            else:
                raise Exception("Automatic driver download is only for Windows. Please download the driver manually and add it to the PATH.")


    def _initialize_driver(self, *args, **kwargs) -> None:
        from selenium.webdriver.edge.service import Service as EdgeService
        import os

        driver_path = os.path.join(os.getcwd(), "msedgedriver.exe")
        if not os.path.exists(driver_path):
            # raise FileNotFoundError(f"Edge driver not found at: {driver_path}")
            self._download_edge_driver()

        service = EdgeService(executable_path=driver_path)
        self.driver = webdriver.Edge(service=service, *args, **kwargs)
        # self.driver.implicitly_wait(self.wait_timeout)
        self.driver.maximize_window()


    def get_driver(self) -> webdriver:
        return self.driver


    def _download_edge_driver(self) -> None:
        get_edge_driver()


    def _download_chrome_driver(self) -> None:
        get_chrome_driver()


    def _wait_for_element(self, by: By, value: str, timeout = 5) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout = 5).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            raise Exception(f"Element {value} not found")
    
    def _wait_for_elements(self, by: By, value: str, timeout = 5) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
        except TimeoutException:
            raise Exception(f"Element {value} not found")


    def _wait_for_element_to_be_clickable(self, by, value, timeout = 5) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
        except TimeoutException:
            raise Exception(f"Element {value} not found")

    
    def _wait_for_element_to_be_visible(self, by, value, timeout = 5) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except TimeoutException:
            raise Exception(f"Element {value} not found")


    def _wait_for_element_to_be_invisible(self, by, value, timeout = 5) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, value))
            )
        except TimeoutException:
            raise Exception(f"Element {value} not found")


    def _wait_for_loading(self, by, value, timeout: int = 10) -> None:
        self._wait_for_element_to_be_visible(by, value, timeout)
        self._wait_for_element_to_be_invisible(by, value, timeout)

    


        
    