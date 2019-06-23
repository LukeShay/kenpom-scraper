from web_scraper.BasePage import BasePage

HOME_URL = 'https://kenpom.com/'
FAN_MATCH_TABLE_ROWS_XPATH = '//table[@id=\'fanmatch-table\']/tbody/tr'
FAN_MATCH_TABLE_ROW_XPATH = FAN_MATCH_TABLE_ROWS_XPATH + '[{}]'
FAN_MATCH_TABLE_PREDICTION = FAN_MATCH_TABLE_ROW_XPATH + '/td[2]'
FAN_MATCH_TABLE_TEAMS = FAN_MATCH_TABLE_ROW_XPATH + '/td[1]/a'
FAN_MATCH_BUTTON_CLASS = 'fanmatch'


class KenPomPage(BasePage):
    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.driver = driver

    def __del__(self):
        BasePage.__del__(self)

    def go_to(self):
        BasePage.go_to_website(self, HOME_URL)

    def go_to_fan_match(self):
        BasePage.click_element_by_class(self, FAN_MATCH_BUTTON_CLASS)

    def login(self, email, password):
        BasePage.send_keys_to_element_by_name(self, 'email', email)
        BasePage.send_keys_to_element_by_name(self, 'password', password)
        BasePage.click_element_by_name(self, 'submit')

    def get_table_row_prediction(self, row_number):
        prediction_element = BasePage.get_element_by_xpath(self, FAN_MATCH_TABLE_PREDICTION.format(row_number))
        return BasePage.get_text(prediction_element), BasePage.get_class(prediction_element)

    def get_table_row_teams(self, row_number):
        teams = BasePage.get_elements_by_xpath(self, FAN_MATCH_TABLE_TEAMS.format(row_number))
        return BasePage.get_text(teams[0]), BasePage.get_text(teams[1])

    def get_num_fan_match_rows(self):
        return len(BasePage.get_elements_by_xpath(self, FAN_MATCH_TABLE_ROWS_XPATH)) - 6
