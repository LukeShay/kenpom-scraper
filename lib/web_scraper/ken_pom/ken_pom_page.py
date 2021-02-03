import os
import json

from lib.web_scraper.base_page import BasePage
from lib.domain.fan_match_model import FanMatch

JSON_FILE_PATH = os.getcwd() + "/../sheets_api/SportsBettingProgram-sheets.json"
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

HOME_URL = "https://kenpom.com/"
BASE_FAN_MATCH_URL = "https://kenpom.com/fanmatch.php"
FAN_MATCH_URL = BASE_FAN_MATCH_URL + "?d={}"

EMAIL_SELECTOR = "#login > input:nth-child(1)"
PASSWORD_SELECTOR = "#login > input:nth-child(2)"
SUBMIT_BUTTON_SELECTOR = "#login > input:nth-child(3)"
FAN_MATCH_BUTTON_SELECTOR = ".fanmatch > a:nth-child(1)"

FAN_MATCH_PREVIOUS_DATE_SELECTOR_1 = "#content-header > a:nth-child(5)"
FAN_MATCH_PREVIOUS_DATE_SELECTOR_2 = "#content-header > a:nth-child(6)"

NO_GAMES_SELECTOR = "#data-area > h2:nth-child(1)"

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
            self.driver = self.driver

    def __del__(self):
        BasePage.__del__(self)

    def go_to(self):
        BasePage.go_to_website(self, HOME_URL)

    def go_to_fan_match(self, date=None):
        if date is None:
            BasePage.go_to_website(self, BASE_FAN_MATCH_URL)
        else:
            BasePage.go_to_website(self, FAN_MATCH_URL.format(date))

    def go_to_ratings(self):
        BasePage.go_to_website(self, BASE_RATINGS_URL)

    def login(self, email, password):
        BasePage.send_keys_to_element_by_selector(self, EMAIL_SELECTOR, email)
        BasePage.send_keys_to_element_by_selector(self, PASSWORD_SELECTOR, password)
        BasePage.click_element_by_selector(self, SUBMIT_BUTTON_SELECTOR)

    def get_current_date(self) -> str:
        try:
            return self.driver.current_url.split("=")[1]
        except:
            return ""

    def go_to_previous_fan_match(self):
        element = None
        try:
            element = BasePage.get_element_by_selector(
                self, FAN_MATCH_PREVIOUS_DATE_SELECTOR_1
            )
        except:
            element = BasePage.get_element_by_selector(
                self, FAN_MATCH_PREVIOUS_DATE_SELECTOR_2
            )

        element.click()

    def go_to_previous_fan_match_with_games(self):
        self.go_to_previous_fan_match()

        while BasePage.does_element_exist_by_selector(self, NO_GAMES_SELECTOR):
            self.go_to_previous_fan_match()

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
            )  # This is awesome - lukeshay
        except:
            return "ERROR"
