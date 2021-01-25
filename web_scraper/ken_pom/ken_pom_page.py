import os
import json

from web_scraper.base_page import BasePage
from web_scraper.ken_pom import ken_pom_utils
from itertools import chain
from domain.ken_pom_prediction import KenPomPrediction

JSON_FILE_PATH = os.getcwd() + "/../sheets_api/SportsBettingProgram-sheets.json"
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

HOME_URL = "https://kenpom.com/"
BASE_FAN_MATCH_URL = "https://kenpom.com/fanmatch.php"
FAN_MATCH_URL = BASE_FAN_MATCH_URL + "?d={}"

EMAIL_XPATH = '//*[@name="email"]'
PASSWORD_XPATH = '//*[@name="password"]'
SUBMIT_BUTTON_XPATH = '//*[@name="submit"]'
FAN_MATCH_BUTTON_XPATH = '//*[@class="fanmatch"]'

FAN_MATCH_TABLE_ROWS_XPATH = '//table[@id="fanmatch-table"]/tbody/tr'
FAN_MATCH_XPATH = FAN_MATCH_TABLE_ROWS_XPATH + "[{}]"
FAN_MATCH_SCORE_XPATH = FAN_MATCH_XPATH + "/td[1]"
FAN_MATCH_TABLE_PREDICTION_XPATH = FAN_MATCH_XPATH + "/td[2]"
FAN_MATCH_TABLE_TEAMS_XPATH = FAN_MATCH_XPATH + "/td[1]/a"
FAN_MATCH_LOCATION_XPATH = FAN_MATCH_XPATH + "/td[4]"

FAN_MATCH_PREVIOUS_DATE_XPATH = '//a[contains(@href,"/fanmatch.php")]'

NO_GAMES_XPATH = '//h2[.="Sorry, no games today. :("]'

BASE_RATINGS_URL = "https://kenpom.com/index.php"
RATINGS_TABLE_ROWS_SELECTOR = "#ratings-table > tbody > tr"
RATINGS_TABLE_TEAMS_SELECTOR = (
    RATINGS_TABLE_ROWS_SELECTOR + " > td:nth-child(2) > a:nth-child(1)"
)

BASE_TEAM_URL = "https://kenpom.com/team.php?team="
TEAM_LOCATION_SELECTOR = "#title-container"


class KenPomPage(BasePage):
    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.driver = driver

        try:
            os.mkdir(f"{os.getcwd()}/output")
        except:
            print()

        self.f = open(f"{os.getcwd()}/output/data.csv", "w")
        f = open(f"{os.getcwd()}/teams.json", "r")
        self.team_locations = json.loads(f.read())

    def __del__(self):
        BasePage.__del__(self)

    def go_to(self):
        BasePage.go_to_website(self, HOME_URL)

    def go_to_fan_match_date(self, date):
        BasePage.go_to_website(self, FAN_MATCH_URL.format(date))

    def go_to_fan_match(self):
        BasePage.go_to_website(self, BASE_FAN_MATCH_URL)

    def go_to_ratings(self):
        BasePage.go_to_website(self, BASE_RATINGS_URL)

    def login(self, email, password):
        BasePage.send_keys_to_element_by_xpath(self, EMAIL_XPATH, email)
        BasePage.send_keys_to_element_by_xpath(self, PASSWORD_XPATH, password)
        BasePage.click_element_by_xpath(self, SUBMIT_BUTTON_XPATH)

    def get_num_fan_match_rows(self) -> int:
        return len(
            BasePage.get_elements_by_xpath(
                self, FAN_MATCH_TABLE_ROWS_XPATH + '/td[@class="stats"]/..'
            )
        )

    def get_current_date(self) -> str:
        return self.driver.current_url.split("=")[1]

    def get_prediction(self, row_number) -> KenPomPrediction:
        prediction = BasePage.get_text_by_xpath(
            self, FAN_MATCH_TABLE_PREDICTION_XPATH.format(row_number)
        )
        teams = BasePage.get_elements_by_xpath(
            self, FAN_MATCH_TABLE_TEAMS_XPATH.format(row_number)
        )
        text = BasePage.get_text_by_xpath(
            self, FAN_MATCH_SCORE_XPATH.format(row_number)
        ).replace(",", "")
        location = BasePage.get_text_by_xpath(
          self, FAN_MATCH_LOCATION_XPATH.format(row_number)
        ).split("\n")[0]

        actual_scores, percentage, score, team = self.parse_row(prediction, text)
        home_team = teams[0].text if location == self.team_locations[teams[0].text] else teams[1].text

        if team == teams[0].text:  # favorite wins
            return KenPomPrediction(
                date=self.get_current_date(),
                favorite=teams[0].text,
                underdog=teams[1].text,
                favorite_actual_score=actual_scores[1],
                underdog_actual_score=actual_scores[3],
                favorite_predicted_score=score[0],
                underdog_predicted_score=score[1],
                percentage=percentage,
                home_team=home_team,
            )
        else:
            return KenPomPrediction(
                date=self.get_current_date(),
                favorite=teams[1].text,
                underdog=teams[0].text,
                favorite_actual_score=actual_scores[3],
                underdog_actual_score=actual_scores[1],
                favorite_predicted_score=score[1],
                underdog_predicted_score=score[0],
                percentage=percentage,
                home_team=home_team,
            )

    @staticmethod
    def parse_row(prediction, text):
        actual_scores = [int(s) for s in text.split() if s.isdigit()]
        predication_array = prediction.split(" ")
        team = ""
        i = 0
        for element in predication_array:
            if "-" in element:
                break

            team += element + " "
            i += 1
        team = team.strip()
        score = [int(s) for s in predication_array[i].split("-")]
        temp_variable = (
            predication_array[i + 1].replace("(", "").replace(")", "").replace("%", "")
        )
        percentage = float(temp_variable)
        return actual_scores, percentage, score, team

    def go_to_previous_fan_match(self):
        element = BasePage.get_element_by_xpath(self, FAN_MATCH_PREVIOUS_DATE_XPATH)
        BasePage.go_to_website(self, element.get_attribute("href"))

    def go_to_previous_fan_match_with_games(self):
        self.go_to_previous_fan_match()

        while BasePage.does_element_exist_by_xpath(self, NO_GAMES_XPATH):
            self.go_to_previous_fan_match()

    def get_previous_date(self) -> str:
        return BasePage.get_text_by_xpath(
            self, BasePage.get_element_by_xpath(self, FAN_MATCH_PREVIOUS_DATE_XPATH)
        )

    def get_row(self, row_number) -> KenPomPrediction:
        try:
            return self.get_prediction(row_number)
        except IndexError:
            return None

    def get_all_teams(self) -> list[str]:
        assert self.driver.current_url == BASE_RATINGS_URL

        teams = []

        for el in BasePage.get_elements_by_selector(self, RATINGS_TABLE_TEAMS_SELECTOR):
            teams.append(el.text)

        return teams

    def go_to_team_page(self, team):
        BasePage.go_to_website(self, f"{BASE_TEAM_URL}{team.replace(' ', '+')}")

    def get_team_location(self) -> str:
        try:
            return (
                BasePage.get_text_by_selector(self, TEAM_LOCATION_SELECTOR)
                .split("\n")[1]
                .split(" · ")[1]
                .strip()
            ) # This is awesome - lukeshay
        except:
            return "ERROR"

    def write_game_data_to_file(self, end_date):
        self.f.write(f"{KenPomPrediction.column_headers()}\n")

        while end_date not in self.driver.current_url:
            for rows in range(1, self.get_num_fan_match_rows() + 1):
                row = self.get_row(rows)

                if row is not None:
                    self.f.write(f"{str(row)}\n")

            self.go_to_previous_fan_match_with_games()
