import time
from KenPom import KenPom
from selenium import webdriver

#from kenpom_utils import *
driver = webdriver.Chrome()

ken_pom = KenPom(driver)

ken_pom.go_to_website()

ken_pom.login('roby@shaybrothers.com', 'DqwtQ5eW1K')

time.sleep(5)

driver.quit()
