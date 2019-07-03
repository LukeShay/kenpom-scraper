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

    @staticmethod
    def get_name(element):
        return element.get_attribute("name")

    @staticmethod
    def get_class(element):
        return element.get_attribute("class")

    @staticmethod
    def get_text(element):
        return element.text

    def go_to_website(self, url):
        self.driver.get(url)

    def send_keys_to_element(self, element_xpath, keys):
        element = self.get_element(element_xpath)
        element.clear()
        element.send_keys(keys)

    def does_element_exist(self, element_xpath):
        try:
            self.driver.implicitly_wait(1)
            self.driver.find_element_by_xpath(element_xpath)
        except NoSuchElementException:
            self.driver.implicitly_wait(WAIT_TIME)
            return False
        self.driver.implicitly_wait(WAIT_TIME)
        return True
