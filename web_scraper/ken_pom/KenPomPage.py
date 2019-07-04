import gspread
from oauth2client.service_account import ServiceAccountCredentials

from web_scraper.BasePage import BasePage
from web_scraper.ken_pom.KenPomUtils import *

HOME_URL = 'https://kenpom.com/'
EMAIL_XPATH = '//*[@name="email"]'
PASSWORD_XPATH = '//*[@name="password"]'
SUBMIT_BUTTON_XPATH = '//*[@name="submit"]'
FAN_MATCH_BUTTON_XPATH = '//*[@class="fanmatch"]'

FAN_MATCH_TABLE_ROWS_XPATH = '//table[@id="fanmatch-table"]/tbody/tr'
FAN_MATCH_TABLE_ROW_XPATH = FAN_MATCH_TABLE_ROWS_XPATH + '[{}]'
FAN_MATCH_TABLE_ROW_SCORE_XPATH = FAN_MATCH_TABLE_ROW_XPATH + '/td[1]'
FAN_MATCH_TABLE_PREDICTION_XPATH = FAN_MATCH_TABLE_ROW_XPATH + '/td[2]'
FAN_MATCH_TABLE_TEAMS_XPATH = FAN_MATCH_TABLE_ROW_XPATH + '/td[1]/a'

FAN_MATCH_PREVIOUS_DATE_XPATH = '//a[contains(@href,"/fanmatch.php")]'

NO_GAMES_XPATH = '//h2[.="Sorry, no games today. :("]'

SHEETS_COLUMNS = ["HOME TEAM", "AWAY TEAM", "HOME SCORE", "AWAY SCORE",
                  "HOME SCORE PREDICTION", "AWAY SCORE PREDICTION", "PERCENTAGE", "CORRECT/WRONG"]

NUM_UNNEEDED_ROWS = 6


class KenPomPage(BasePage):
    def __init__(self, driver):
        self.init_sheet()
        BasePage.__init__(self, driver)
        self.driver = driver

    def init_sheet(self):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('sheets_api/SportsBettingProgram-sheets.json',
                                                                      self.scope)
        self.client = gspread.authorize(self.creds)

        self.sheet = self.client.open("KenPom").sheet1
        self.sheet.clear()
        self.row = 1

        self.sheet.insert_row(SHEETS_COLUMNS, self.row)
        self.row += 1

    def __del__(self):
        BasePage.__del__(self)

    def go_to(self):
        BasePage.go_to_website(self, HOME_URL)

    def go_to_fan_match(self):
        BasePage.click_element(self, FAN_MATCH_BUTTON_XPATH)

    def login(self, email, password):
        BasePage.send_keys_to_element(self, EMAIL_XPATH, email)
        BasePage.send_keys_to_element(self, PASSWORD_XPATH, password)
        BasePage.click_element(self, SUBMIT_BUTTON_XPATH)

    def get_num_rows(self):
        return len(BasePage.get_elements(self, FAN_MATCH_TABLE_ROWS_XPATH + '/td[@class="stats"]/..'))

    def get_table_row_prediction(self, row_number):
        prediction = BasePage.get_text(self, FAN_MATCH_TABLE_PREDICTION_XPATH.format(row_number))  # .replace("'", '')
        predication_array = prediction.split(' ')
        team = ''
        i = 0

        for element in predication_array:
            if '-' in element:
                break

            team += element + ' '
            i += 1

        team = team.strip()
        score = [int(s) for s in predication_array[i].split('-')]
        percentage = predication_array[i + 1].replace('(', '').replace(')', '')

        if team == self.get_table_row_teams(row_number)[0]:
            return score[0], score[1], percentage, \
                   BasePage.get_class(self, FAN_MATCH_TABLE_PREDICTION_XPATH.format(row_number))
        else:
            return score[1], score[0], percentage, \
                   BasePage.get_class(self, FAN_MATCH_TABLE_PREDICTION_XPATH.format(row_number))

    def get_table_row_teams(self, row_number):
        teams = BasePage.get_elements(self, FAN_MATCH_TABLE_TEAMS_XPATH.format(row_number))
        return teams[0].text, teams[1].text

    def get_table_row_score(self, row_number):
        text = BasePage.get_text(self, FAN_MATCH_TABLE_ROW_SCORE_XPATH.format(row_number)).replace(',', '')

        numbers = [int(s) for s in text.split() if s.isdigit()]
        return numbers[1], numbers[3]

    def get_num_fan_match_rows(self):
        return len(BasePage.get_elements(self, FAN_MATCH_TABLE_ROWS_XPATH)) - 6

    def go_to_previous_fan_match(self):
        element = BasePage.get_element(self, FAN_MATCH_PREVIOUS_DATE_XPATH)
        BasePage.go_to_website(self, element.get_attribute('href'))

    def go_to_previous_fan_match_with_games(self):
        self.go_to_previous_fan_match()

        while BasePage.does_element_exist(self, NO_GAMES_XPATH):
            self.go_to_previous_fan_match()

    def get_previous_date(self):
        return BasePage.get_text(BasePage.get_element(self, FAN_MATCH_PREVIOUS_DATE_XPATH))

    def get_row_as_tuple(self, row_number):
        return self.get_table_row_teams(row_number) + self.get_table_row_score(row_number) + \
               self.get_table_row_prediction(row_number)

    def get_row_as_string(self, row_number):
        return tuple_to_string(self.get_row_as_tuple(row_number))

    def get_current_date(self):
        return self.driver.current_url.split('=')[1]

    def send_all_rows_to_sheet(self):
        for num in range(1, self.get_num_rows() + 1):
            self.sheet.insert_row(self.get_row_as_tuple(num), self.row)
            self.row += 1

        self.sheet.insert_row([], self.row)
        self.row += 1

    def get_all_rows_as_string(self):
        string = ''
        for num in range(1, self.get_num_rows() + 1):
            string += self.get_row_as_string(num) + '\n'

        return string
