import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from web_scraper.BasePage import BasePage
from web_scraper.ken_pom.KenPomUtils import *

JSON_FILE_PATH = os.getcwd() + '/../sheets_api/SportsBettingProgram-sheets.json'
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

HOME_URL = 'https://kenpom.com/'
EMAIL_XPATH = '//*[@name="email"]'
PASSWORD_XPATH = '//*[@name="password"]'
SUBMIT_BUTTON_XPATH = '//*[@name="submit"]'
FAN_MATCH_BUTTON_XPATH = '//*[@class="fanmatch"]'

FAN_MATCH_TABLE_ROWS_XPATH = '//table[@id="fanmatch-table"]/tbody/tr'
FAN_MATCH_XPATH = FAN_MATCH_TABLE_ROWS_XPATH + '[{}]'
FAN_MATCH_SCORE_XPATH = FAN_MATCH_XPATH + '/td[1]'
FAN_MATCH_TABLE_PREDICTION_XPATH = FAN_MATCH_XPATH + '/td[2]'
FAN_MATCH_TABLE_TEAMS_XPATH = FAN_MATCH_XPATH + '/td[1]/a'

FAN_MATCH_PREVIOUS_DATE_XPATH = '//a[contains(@href,"/fanmatch.php")]'

NO_GAMES_XPATH = '//h2[.="Sorry, no games today. :("]'

COVERED = "=C[{}]<D[{}]"

SHEETS_COLUMNS = ["FAVORITE", "UNDERDOG", "ACTUAL SPREAD", "PREDICTED SPREAD", "PERCENTAGE", "CORRECT TEAM", "COVERED"]

NUM_UNNEEDED_ROWS = 6


class KenPomPage(BasePage):
    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.driver = driver
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE_PATH, SCOPE)
        self.client = gspread.authorize(self.credentials)

        self.worksheet = self.client.open("KenPom")
        self.sheet1 = self.client.open("KenPom").sheet1
        self.row = 1

        self.sheet1.insert_row(SHEETS_COLUMNS, self.row)
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

    def get_prediction(self, row_number):
        prediction = BasePage.get_text(self, FAN_MATCH_TABLE_PREDICTION_XPATH.format(row_number))
        teams = BasePage.get_elements(self, FAN_MATCH_TABLE_TEAMS_XPATH.format(row_number))
        text = BasePage.get_text(self, FAN_MATCH_SCORE_XPATH.format(row_number)).replace(',', '')

        actual_scores = [int(s) for s in text.split() if s.isdigit()]

        # TODO parse_prediction(prediction)

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
        percentage = float(predication_array[i + 1].replace('(', '').replace(')', '').replace('%', ''))

        if team == teams[0].text:
            return teams[0].text, teams[1].text, actual_scores[3] - actual_scores[1], score[1] - score[0], \
                   percentage, actual_scores[3] - actual_scores[1] < 0
        else:
            return teams[1].text, teams[0].text, actual_scores[1] - actual_scores[3], score[1] - score[0], \
                   percentage, actual_scores[1] - actual_scores[3] < 0

    def get_num_fan_match_rows(self):
        return len(BasePage.get_elements(self, FAN_MATCH_TABLE_ROWS_XPATH)) - 6

    def go_to_previous_fan_match(self):
        element = BasePage.get_element(self, FAN_MATCH_PREVIOUS_DATE_XPATH)  # TODO
        BasePage.go_to_website(self, element.get_attribute('href'))

    def go_to_previous_fan_match_with_games(self):
        self.go_to_previous_fan_match()

        while BasePage.does_element_exist(self, NO_GAMES_XPATH):
            self.go_to_previous_fan_match()

    def get_previous_date(self):
        return BasePage.get_text(self, BasePage.get_element(self, FAN_MATCH_PREVIOUS_DATE_XPATH))

    def get_row_as_tuple(self, row_number):
        try:
            r_tuple = self.get_prediction(row_number)
            covered = r_tuple[2] < r_tuple[3] < 0
            return r_tuple + tuple((covered,))
        except IndexError:
            return tuple((IndexError, 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR'))

    def get_row_as_string(self, row_number):
        return tuple_to_string(self.get_row_as_tuple(row_number))

    def get_current_date(self):
        return self.driver.current_url.split('=')[1]

    def send_all_rows_to_sheet(self):
        for num in range(1, self.get_num_rows() + 1):
            self.sheet1.insert_row(self.get_row_as_tuple(num), self.row, 'USER_ENTERED')
            self.row += 1

    def get_all_rows_as_string(self):
        string = ''
        for num in range(1, self.get_num_rows() + 1):
            string += self.get_row_as_string(num) + '\n'

        return string

    def send_all_rows_of_pages_to_sheets(self, end_date):
        self.sheet1.clear()
        fanmatch_list = [SHEETS_COLUMNS]

        while end_date not in self.driver.current_url:
            for rows in range(1, self.get_num_rows() + 1):
                fanmatch_list.append(self.get_row_as_tuple(rows))

            self.go_to_previous_fan_match_with_games()

        self.sheet1.clear()

        self.worksheet.values_update(
            'Sheet1',
            params={
                'valueInputOption': 'USER_ENTERED'
            },
            body={
                'values': fanmatch_list
            }
        )

