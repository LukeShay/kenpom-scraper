import time
from KenPom import KenPom
from selenium import webdriver

ken_pom = KenPom(webdriver.Chrome())

ken_pom.go_to()

ken_pom.login('roby@shaybrothers.com', 'DqwtQ5eW1K') #TODO Needs to be changed to take in arguments in command line.

ken_pom.go_to_fan_match()

print(ken_pom.get_num_fan_match_rows())

time.sleep(5)
