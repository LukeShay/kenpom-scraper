import sys
import os
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from lib.web_scraper.ken_pom.ken_pom_page import KenPomPage
from lib.utils.env import Env
from lib.domain.team_model import Team

DRIVER_PATH = "./drivers/chromedriver"


def main():
    f = open(f"{os.getcwd()}/teams.json", "w")

    chrome_options = Options()
    chrome_options.add_argument(Env.selenium_flags())

    web_driver = webdriver.Chrome(options=chrome_options, executable_path=DRIVER_PATH)
    web_driver.maximize_window()

    ken_pom = KenPomPage(web_driver)

    ken_pom.go_to()
    ken_pom.login(Env.ken_pom_email(), Env.ken_pom_password())

    ken_pom.go_to_ratings()

    teams = ken_pom.get_all_teams()

    arr = []

    for team in teams:
        ken_pom.go_to_team_page(team)
        arr.append(Team(team, ken_pom.get_team_location())

    f.write(json.dumps(arr))


if __name__ == "__main__":
    main()
