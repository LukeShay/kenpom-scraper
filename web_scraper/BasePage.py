WAIT_TIME = 10


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(WAIT_TIME)

    def __del__(self):
        self.driver.close()

    def click_element_by_class(self, element_class):
        self.get_element_by_class(element_class).click()

    def click_element_by_name(self, element_name):
        self.get_element_by_name(element_name).click()

    def get_element_by_class(self, element_class):
        return self.driver.find_element_by_class_name(element_class)

    def get_element_by_name(self, element_name):
        return self.driver.find_element_by_name(element_name)

    def get_element_by_xpath(self, element_xpath):
        return self.driver.find_element_by_xpath(element_xpath)

    def get_elements_by_xpath(self, elements_xpath):
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

    def send_keys_to_element_by_name(self, element_name, keys):
        element = self.get_element_by_name(element_name)
        element.clear()
        element.send_keys(keys)
