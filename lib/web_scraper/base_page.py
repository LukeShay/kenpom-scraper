from selenium.common.exceptions import NoSuchElementException

WAIT_TIME = 10


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(WAIT_TIME)

    def __del__(self):
        self.driver.close()

    def go_to_website(self, url):
        self.driver.get(url)

    def get_element_by_selector(self, element_selector):
        return self.driver.find_element_by_css_selector(element_selector)

    def get_elements_by_selector(self, elements_selector):
        return self.driver.find_elements_by_css_selector(elements_selector)

    def get_text_by_selector(self, element_selector):
        return self.driver.find_element_by_css_selector(element_selector).text

    def click_element_by_selector(self, element_selector):
        self.get_element_by_selector(element_selector).click()

    def send_keys_to_element_by_selector(self, element_selector, keys):
        element = self.get_element_by_selector(element_selector)
        element.clear()
        element.send_keys(keys)

    def does_element_exist_by_selector(self, element_selector):
        try:
            self.driver.implicitly_wait(0)
            self.driver.find_element_by_css_selector(element_selector)
        except NoSuchElementException:
            self.driver.implicitly_wait(WAIT_TIME)
            return False
        self.driver.implicitly_wait(WAIT_TIME)
        return True
