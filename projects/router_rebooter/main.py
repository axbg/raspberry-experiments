from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from os import getenv
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime


def wait_element(get_element, driver):
    retries = 0
    element = None
    while not element:
        sleep(1)
        retries += 1
        try:
            element = get_element(driver)
        except NoSuchElementException as ex:
            if retries == 10:
                raise ex
            pass
    return element


def wait_element_by_id(element, driver):
    return wait_element(lambda x: x.find_element(By.ID, element), driver)


def main():
    # Load data from the .env file
    load_dotenv()

    # Load all env variables
    ROUTER_PASSWORD = getenv("ROUTER_PASSWORD")
    ROUTER_URL = getenv("ROUTER_URL")

    # Initialize log_file
    with open("last_log", "a") as log:
        log.write(f"\n\n--------- Log {datetime.now()} ---------\n")

        # Configure browser options
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # Get browser variable and navigate to ROUTER_URL
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(ROUTER_URL)
        log.write("Opened browser\n")

        # Populate the password field
        pwd_inpt = wait_element_by_id("pcPassword", browser)
        pwd_inpt.send_keys(ROUTER_PASSWORD)
        log.write("Inserted password\n")

        # Post the login form
        login_btn = browser.find_element(By.ID, "loginBtn")
        login_btn.click()
        log.write("Logged in\n")

        # Navigate to System tools
        browser.switch_to.frame(wait_element_by_id("frame1", browser))
        system_tools_btn = wait_element_by_id("menu_tools", browser)
        system_tools_btn.click()
        log.write("Opened menu sidebar\n")

        system_reboot_menu_btn = browser.find_element(By.ID, "menu_restart")
        system_reboot_menu_btn.click()
        log.write("Navigated to Reboot menu\n")

        # Find and click reboot button
        browser.switch_to.default_content()
        browser.switch_to.frame(wait_element_by_id("frame2", browser))
        system_reboot_btn = wait_element_by_id("button_reboot", browser)
        system_reboot_btn.click()
        log.write("Clicked on Reboot\n")

        # Click accept on the confirmation alert
        browser.switch_to.alert.accept()
        log.write("Accepted on Reboot alert\n")
        log.write("Reboot started\n")
        log.write("--------------------------------------------------\n")


if __name__ == '__main__':
    main()
