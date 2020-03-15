import time

from selenium.common.exceptions import NoSuchElementException


class AbstractProvider:
    name = None
    url = None

    @staticmethod
    def scrap(driver, username, password, domain, ip):
        pass

    @classmethod
    def wait_element(cls, get_element, driver):
        retries = 0
        element = None
        while not element:
            time.sleep(1)
            retries += 1
            try:
                element = get_element(driver)
            except NoSuchElementException as ex:
                if retries == 10:
                    raise ex
                pass
        return element

    @classmethod
    def get_implementation(cls, provider_name):
        for clz in cls.__subclasses__():
            if clz.__name__.lower() == str(provider_name).lower():
                return clz
