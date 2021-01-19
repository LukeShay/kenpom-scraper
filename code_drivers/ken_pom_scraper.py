import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from web_scraper.ken_pom.ken_pom_page import *

CURRENT_FIRST_DATE = "2019-04-08"
DRIVER_PATH = os.getcwd() + "/../web_drivers/chromedriver.exe"


def main():
    assert len(sys.argv) == 3, "Incorrect number of args inputted."

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
    ken_pom.write_game_data_to_file("2020-11-25")

    web_driver.close()


if __name__ == "__main__":
    main()
