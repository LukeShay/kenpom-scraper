import sys

from selenium import webdriver

from web_scraper.ken_pom.KenPomPage import KenPomPage
from web_scraper.ken_pom.KenPomUtils import *

ken_pom = KenPomPage(webdriver.Chrome())
ken_pom.go_to()
ken_pom.login(sys.argv[1], sys.argv[2])
ken_pom.go_to_fan_match()

file = open("KenPomPredictions.txt", "w+")

file.write(
    tuple_to_string(ken_pom.get_table_row_teams(1)) + tuple_to_string(ken_pom.get_table_row_prediction(1)) + '\n')

file.close()
