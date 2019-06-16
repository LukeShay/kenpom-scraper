from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseUtils:
    def __init__(self, driver):
        self.driver = driver

    def go_to_website(self, url):
        self.driver.get(url)

    def get_element_by_name_wait(self, element_name):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, element_name)))

    def get_element_by_name(self, element_name):
        return self.driver.find_element_by_name(element_name)
