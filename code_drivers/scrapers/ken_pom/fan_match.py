import datetime
import logging
import os
import sys
from concurrent import futures

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from lib.web_scraper.ken_pom.ken_pom_page import KenPomPage
from lib.utils.env import Env
from lib.utils.fs import FS

DRIVER_PATH = "./drivers/chromedriver"


def run(date, fan_match_soup, fan_match_dao):
    process = date.strftime("%Y-%m-%d %H:%M:%S.%f %z")

    print(f"{process} starting...")

    for prediction in fan_match_soup.run(date):
        saved = fan_match_dao.save_or_update(prediction)
        print(saved)

    fan_match_dao.commit()
    print(f"{process} finished...")


def main():
    FS.create_dir("./output/html")

    chrome_options = Options()
    if Env.selenium_flags() != "":
        chrome_options.add_argument(Env.selenium_flags())

    web_driver = webdriver.Chrome(options=chrome_options, executable_path=DRIVER_PATH)
    web_driver.maximize_window()

    ken_pom = KenPomPage(web_driver)

    ken_pom.go_to()
    ken_pom.login(Env.ken_pom_email(), Env.ken_pom_password())

    ken_pom.go_to_fan_match()

    while ken_pom.get_current_date() != "2020-11-25":
        ken_pom.go_to_previous_fan_match_with_games()

        [year, month, day] = ken_pom.get_current_date().split("-")

        date = datetime.datetime(int(year), int(month), int(day))

        with open(f"./output/html/{ken_pom.get_current_date()}.html", "w") as f:
            f.write(ken_pom.driver.page_source)


if __name__ == "__main__":
    main()
