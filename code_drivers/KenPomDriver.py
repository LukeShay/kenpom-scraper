import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from web_scraper.ken_pom.KenPomPage import *

CURRENT_FIRST_DATE = '2019-04-08'


def main():
    assert len(sys.argv) == 4, 'Incorrect number of args inputted.'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920x1080')

    chrome_driver = os.getcwd() + '/Users/luke/Desktop/Sports-Betting-Program/web_drivers/chromedriver.exe'

    web_driver = webdriver.Chrome(options=chrome_options)

    ken_pom = KenPomPage(web_driver)

    ken_pom.go_to()
    ken_pom.login(sys.argv[1], sys.argv[2])

    ken_pom.go_to_fan_match()
    ken_pom.send_all_rows_of_pages_to_sheets(sys.argv[3])

    ken_pom.__del__()


if __name__ == "__main__":
    main()
