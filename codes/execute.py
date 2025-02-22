import time
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


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

    def wait_element_visible_and_click(
        self, xpath: str, timeout: int = 5
    ) -> WebElement:
        wait = WebDriverWait(self.driver, timeout=timeout)
        wait.until(EC.element_to_be_clickable(("xpath", xpath))).click()

    def click_element(self, xpath: str, sleep_time: int = 0):
        element = self.find_element(xpath)
        time.sleep(sleep_time)
        element.click()

    def select_item_in_menu(self, menu, target_text: str):
        menu = Select(self.wait_element_visible(menu))
        menu.select_by_visible_text(target_text)
