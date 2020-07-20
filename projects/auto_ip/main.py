#!/home/pi/Documents/dev/auto_ip/sandbox/bin/python
import os

from dotenv import load_dotenv
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import providers

load_dotenv(".env")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome("chromedriver", options=chrome_options)

try:
    ip = get('https://api.ipify.org').text

    index = 0
    while True:
        conf = str(os.environ.get("CONF_{}".format(index))).split("#")

        if len(conf) != 4:
            break

        domain = conf[0]
        domain_provider = conf[1]
        username = conf[2]
        password = conf[3]

        clz = providers.abstract_provider.AbstractProvider.get_implementation(domain_provider)

        if clz:
            clz.scrap(driver, username, password, domain, ip)
        else:
            print("Provider {} doesn't have an implementation".format(domain_provider))

        index += 1
finally:
    driver.close()
    print("Execution finished")
