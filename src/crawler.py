from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from typing import Literal, Any
from pathlib import Path


class StockeExchangeCrawler:
    __driver = None

    def __init__(self, driver: Literal['firefox', 'chrome']) -> None:
        match driver:
            case 'firefox':
                self.driver = webdriver.Firefox()

            case 'chrome':
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")

                root = Path('.')
                driver_path = root.parent.joinpath(
                    'drivers/chrome/chromedriver').absolute()
                service = Service(str(driver_path))

                self.driver = webdriver.Chrome(
                    service=service, options=chrome_options)

    def __del__(self) -> None:
        if self.driver is not None:
            self.driver.quit()

    @property
    def driver(self) -> webdriver.Firefox | webdriver.Chrome:
        return self.__driver

    @driver.setter
    def driver(self, driver: Any) -> None:
        self.__driver = driver

    def open_stock_exchange_page(self) -> None:
        """
            Open main page of 'finance.yahoo.com'
        """
        self.driver.implicitly_wait(10)
        self.driver.get("https://finance.yahoo.com/screener/new")

    def remove_filters(self):
        """
            remove default select filters
        """
        # remove filters
        while True:
            try:
                remove_button = self.driver.find_element(
                    By.CLASS_NAME, 'removeFilter')
                remove_button.click()
            except Exception as error:
                break

    def filter_region(self, region: str) -> None:
        """
            add filter of region
        """
        # add new filter
        button_add = self.driver.find_element(By.CLASS_NAME, 'addFilter')
        button_add.click()
        time.sleep(1)

        # filter region
        region_checkbox = self.driver.find_element(
            By.XPATH, "//li[label//span[text()='Region']]//input[@type='checkbox']")
        if not region_checkbox.is_selected():
            region_checkbox.click()
            time.sleep(1)

        # close filters
        button_close = self.driver.find_element(
            By.XPATH, "//div[button//span[text()='Close']]//button")
        button_close.click()
        time.sleep(1)

        # filter region
        add_region = self.driver.find_element(
            By.XPATH, "//li[button//span//span//span[text()='Region']]//button")
        add_region.click()
        time.sleep(1)

        # input region
        input_region = self.driver.find_element(
            By.XPATH, f"//li[label//span[text()='{region}']]//input[@type='checkbox']")
        input_region.click()
        time.sleep(1)

        # button to filter and search
        button_filter = self.driver.find_element(
            By.XPATH, "//button[span[text()='Find ']//span[text()='Stocks']]")
        button_filter.click()
        time.sleep(1)

    def get_max_results_per_page(self) -> None:
        """
            select max result per page
        """
        time.sleep(5)
        button = self.driver.find_element(
            By.XPATH, "//*[@id='scr-res-table']/div[2]/span/div/span")
        button.click()

        options = self.driver.find_elements(
            By.XPATH, "//*[@id='scr-res-table']/div[2]/span/div[2]/div")
        options[-1].click()

    def next_page(self) -> bool:
        """
            access next result table page
        """
        time.sleep(5)
        button = self.driver.find_element(
            By.XPATH, "//*[@id='scr-res-table']/div[2]/button[3]")

        if button.get_attribute("aria-disabled") == "true":
            return False

        button.click()
        return True

    def get_html(self) -> str:
        """
            get the html of the page
        """
        time.sleep(5)
        html = self.driver.page_source
        return html


if __name__ == '__main__':
    crawler = StockeExchangeCrawler('firefox')
    crawler.open_stock_exchange_page()
    crawler.remove_filters()
    crawler.filter_region('Brazil')
    crawler.get_max_results_per_page()
    crawler.get_html()
