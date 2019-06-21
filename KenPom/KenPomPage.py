from BasePage import BasePage

KEN_POM_FAN_MATCH = 'https://kenpom.com/fanmatch.php?d=2019-04-06'
KEN_POM_HOME = 'https://kenpom.com/'
POMEROY_TABLE__ROWS_XPATH = "//table[@id='fanmatch-table']/tbody/tr"
FAN_MATCH_BUTTON_CLASS = 'fanmatch'


class KenPomPage(BasePage):
    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.driver = driver

    def __del__(self):
        BasePage.__del__(self)

    def go_to(self):
        BasePage.go_to_website(self, KEN_POM_HOME)

    def go_to_fan_match(self):
        BasePage.go_to_website(self, KEN_POM_FAN_MATCH)

    def login(self, email, password):
        BasePage.send_keys_to_element_by_name(self, 'email', email)
        BasePage.send_keys_to_element_by_name(self, 'password', password)
        BasePage.click_element_by_name(self, 'submit')

    def get_table_row_prediction(self, row_number):
        prediction_element = BasePage.get_element_by_xpath(self, POMEROY_TABLE__ROWS_XPATH + "[" + str(
            row_number) + "]//td[2]")
        teams = BasePage.get_elements_by_xpath(self, POMEROY_TABLE__ROWS_XPATH + "[" + str(
            row_number) + "]//td[1]/a")
        return BasePage.get_text(teams[0]), BasePage.get_text(teams[1]), BasePage.get_text(prediction_element), BasePage.get_class(prediction_element)

    def get_num_fan_match_rows(self):
        return len(BasePage.get_elements_by_xpath(self, POMEROY_TABLE__ROWS_XPATH)) - 6
