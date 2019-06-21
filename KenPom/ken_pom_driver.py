import time
from KenPomPage import KenPomPage
from selenium import webdriver
import sys

ken_pom = KenPomPage(webdriver.Chrome())

ken_pom.go_to()

ken_pom.login(sys.argv[1], sys.argv[2])

ken_pom.go_to_fan_match()

print(ken_pom.get_num_fan_match_rows())
print(ken_pom.get_table_row_prediction(1))

time.sleep(5)