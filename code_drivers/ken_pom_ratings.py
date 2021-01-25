import sys
import os
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from web_scraper.ken_pom.ken_pom_page import KenPomPage

DRIVER_PATH = os.getcwd() + "/../web_drivers/chromedriver.exe"


def main():
    assert len(sys.argv) == 3, "Incorrect number of args inputted."

    f = open(f"{os.getcwd()}/teams.json", "w")

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    web_driver = webdriver.Chrome(
        options=chrome_options
    )  # , executable_path=DRIVER_PATH)
    web_driver.maximize_window()

    ken_pom = KenPomPage(web_driver)

    ken_pom.go_to()
    ken_pom.login(sys.argv[1], sys.argv[2])

    ken_pom.go_to_ratings()

    teams = ken_pom.get_all_teams()

    arr = []

    for team in teams:
        ken_pom.go_to_team_page(team)
        arr.append({ "team": team, "location": ken_pom.get_team_location() })

    f.write(json.dumps(arr))

if __name__ == "__main__":
    main()
