from BaseUtils import BaseUtils

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

KEN_POM_FAN_MATCH = 'https://kenpom.com/fanmatch.php?d=2019-04-06'
KEN_POM_HOME = 'https://kenpom.com/'
POMEROY_RATINGS_TABLE__ROWS_XPATH = "//table[@id='fanmatch-table']//tr"
FAN_MATCH_BUTTON_CLASS = 'fanmatch'


class KenPom(BaseUtils):
    def __init__(self, driver):
        BaseUtils.__init__(self, driver)

    def go_to(self):
        BaseUtils.go_to_website(self, KEN_POM_HOME)
        
    def go_to_fan_match(self):
        BaseUtils.go_to_website(self, KEN_POM_FAN_MATCH)

    def login(self, email, password):
        BaseUtils.send_keys_to_element_by_name(self, 'email', email)
        BaseUtils.send_keys_to_element_by_name(self, 'password', password)
        BaseUtils.click_element_by_name(self, 'submit')

    def get_num_fan_match_rows(self):
        return len(BaseUtils.get_elements_by_xpath(self, POMEROY_RATINGS_TABLE__ROWS_XPATH))



