import sys

from selenium import webdriver

from web_scraper.ken_pom.KenPomPage import *

CURRENT_FIRST_DATE = '2019-04-08'

file = open('data/KenPomPredictions.txt', 'w+')
ken_pom = KenPomPage(webdriver.Chrome())

ken_pom.go_to()
ken_pom.login(sys.argv[1], sys.argv[2])

ken_pom.go_to_fan_match()
file.write(str("".join(SHEETS_COLUMNS)) + '\n')

ken_pom.send_all_rows_to_sheet()
file.write(ken_pom.get_all_rows_as_string())

for num in range(20):
    ken_pom.go_to_previous_fan_match_with_games()
    ken_pom.send_all_rows_to_sheet()
    file.write(ken_pom.get_all_rows_as_string())

file.close()
ken_pom.__del__()
