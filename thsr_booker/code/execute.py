import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException


class Driver:
    def __init__(self, driver_arg: str):
        self._setup_driver(driver_arg)
        self.driver.implicitly_wait(5)

    def _setup_driver(self, driver_arg: str):
        options = webdriver.ChromeOptions()
        options.add_argument(driver_arg)
        self.driver = webdriver.Chrome(options=options)

    def go_to_url(self, url: str):
        self.driver.get(url=url)

    def wait_element_visible(self, xpath: str, timeout: int = 5) -> WebElement:
        wait = WebDriverWait(self.driver, timeout=timeout)
        return wait.until(EC.element_to_be_clickable(("xpath", xpath)))

    def wait_elements_visible(self, xpath: str, timeout: int = 5) -> list[WebElement]:
        wait = WebDriverWait(self.driver, timeout=timeout)
        return wait.until(EC.presence_of_all_elements_located(("xpath", xpath)))

    def wait_element_visible_and_click(
        self, xpath: str, timeout: int = 5
    ) -> WebElement:
        wait = WebDriverWait(self.driver, timeout=timeout)
        wait.until(EC.element_to_be_clickable(("xpath", xpath))).click()

    def click_element(self, xpath: str, sleep_time: int = 0):
        element = self.wait_element_visible(xpath)
        time.sleep(sleep_time)
        element.click()

    def select_item_in_menu(self, menu, target_text: str):
        menu = Select(self.wait_element_visible(menu))
        menu.select_by_visible_text(target_text)

    def input_text(self, xpath: str, text: str):
        element = self.wait_element_visible(xpath)
        element.send_keys(text)

    def check_element_is_exist(self, xpath: str, timeout: int = 5) -> bool:
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(("xpath", xpath))
            )
            return element.is_displayed()
        except TimeoutException:
            return False

    def get_element_text(self, xpath: str) -> Optional[str]:
        try:
            element = self.wait_element_visible(xpath=xpath)
            return str(element.text)
        except:
            return None

    def close(self):
        self.driver.quit()
