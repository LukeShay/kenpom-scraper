from selenium.common.exceptions import NoSuchElementException

WAIT_TIME = 10


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(WAIT_TIME)

    def __del__(self):
        self.driver.close()

    def click_element(self, element_xpath):
        self.get_element(element_xpath).click()

    def get_element(self, element_xpath):
        return self.driver.find_element_by_xpath(element_xpath)

    def get_elements(self, elements_xpath):
        return self.driver.find_elements_by_xpath(elements_xpath)

    def get_name(self, element_xpath):
        return self.get_element(element_xpath).get_attribute("name")

    def get_class(self, element_xpath):
        return self.get_element(element_xpath).get_attribute("class")

    def get_text(self, element_xpath):
        return self.get_element(element_xpath).text

    def go_to_website(self, url):
        self.driver.get(url)

    def send_keys_to_element(self, element_xpath, keys):
        element = self.get_element(element_xpath)
        element.clear()
        element.send_keys(keys)

    def does_element_exist(self, element_xpath):
        try:
            self.driver.implicitly_wait(0)
            self.driver.find_element_by_xpath(element_xpath)
        except NoSuchElementException:
            self.driver.implicitly_wait(WAIT_TIME)
            return False
        self.driver.implicitly_wait(WAIT_TIME)
        return True
