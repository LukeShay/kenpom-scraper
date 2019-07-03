import sys
from web_scraper.ken_pom.KenPomUtils import *
from selenium import webdriver

from web_scraper.ken_pom.KenPomPage import KenPomPage

CURRENT_FIRST_DATE = '2019-04-08'

file = open('data/KenPomPredictions.txt', 'w+')
ken_pom = KenPomPage(webdriver.Chrome())

ken_pom.go_to()
ken_pom.login(sys.argv[1], sys.argv[2])

ken_pom.go_to_fan_match()
write_to_file_and_print(file, CURRENT_FIRST_DATE)
write_to_file_and_print(file, ken_pom.get_all_rows_as_string())

for num in range(20):
    ken_pom.go_to_previous_fan_match_with_games()
    write_to_file_and_print(file, ken_pom.get_current_date())
    write_to_file_and_print(file, ken_pom.get_all_rows_as_string() + '\n')

file.close()
ken_pom.__del__()
