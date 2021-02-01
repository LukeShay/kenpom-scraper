import sys
import os
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine

from lib.web_scraper.ken_pom.ken_pom_page import KenPomPage
from lib.dao.fan_match_dao import FanMatchDAO
from lib.domain.base import Base
from lib.soup.fan_match_soup import FanMatchSoup

DRIVER_PATH = os.getcwd() + "/../web_drivers/chromedriver.exe"


def main():
    assert len(sys.argv) == 3, "Incorrect number of args inputted."

    engine = create_engine("sqlite:///fan_match.db")
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    fan_match_dao = FanMatchDAO(engine)

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    web_driver = webdriver.Chrome(
        options=chrome_options
    )  # , executable_path=DRIVER_PATH)
    web_driver.maximize_window()

    ken_pom = KenPomPage(web_driver)

    ken_pom.go_to()
    ken_pom.login(sys.argv[1], sys.argv[2])

    ken_pom.go_to_fan_match()

    while ken_pom.get_current_date() != "2020-11-25":
        ken_pom.go_to_previous_fan_match_with_games()

        [year, month, day] = ken_pom.get_current_date().split("-")

        date = datetime.datetime(int(year), int(month), int(day))

        for prediction in FanMatchSoup(ken_pom.driver.page_source).run(date):
            saved = fan_match_dao.save_or_update(prediction)
            print(saved)

        fan_match_dao.commit()


if __name__ == "__main__":
    main()
