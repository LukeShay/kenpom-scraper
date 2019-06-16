from BaseUtils import BaseUtils

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

KEN_POM_URL = 'https://kenpom.com/fanmatch.php?d=2019-04-06'
KEN_POM_HOME = 'https://kenpom.com/'


class KenPom(BaseUtils):
    def __init__(self, driver):
        BaseUtils.__init__(self, driver)

    def go_to_website(self):
        BaseUtils.go_to_website(self, KEN_POM_HOME)

    def login(self, email, password):
        email_box = BaseUtils.get_element_by_name_wait(self, 'email')
        password_box = BaseUtils.get_element_by_name(self, 'password')
        submit_button = BaseUtils.get_element_by_name(self, 'submit')

        email_box.clear()
        email_box.send_keys(email)

        password_box.clear()
        password_box.send_keys(password)

        submit_button.send_keys(Keys.ENTER)
