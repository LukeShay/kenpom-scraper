import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from web_scraper.ken_pom.KenPomPage import *

CURRENT_FIRST_DATE = '2019-04-08'
DRIVER_PATH = os.getcwd() + '/../web_drivers/chromedriver.exe'


def main():
    assert len(sys.argv) == 3, 'Incorrect number of args inputted.'
    #        start          end           start         end           start         end           start         end
    dates = ['2019-04-08', '2019-03-09', '2019-03-08', '2019-02-09', '2019-02-08', '2019-01-09', '2019-01-08',
             '2018-12-01']

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    web_driver = webdriver.Chrome(options=chrome_options)  # , executable_path=DRIVER_PATH)
    web_driver.maximize_window()

    ken_pom = KenPomPage(web_driver)

    ken_pom.go_to()
    ken_pom.login(sys.argv[1], sys.argv[2])

    ken_pom.go_to_fan_match_date(dates[0])
    ken_pom.write_game_data_to_file(dates[1])

    ken_pom.go_to_fan_match_date(dates[2])
    ken_pom.write_game_data_to_file(dates[3])

    ken_pom.go_to_fan_match_date(dates[4])
    ken_pom.write_game_data_to_file(dates[5])

    ken_pom.go_to_fan_match_date(dates[6])
    ken_pom.write_game_data_to_file(dates[7])

    web_driver.close()


if __name__ == "__main__":
    main()
