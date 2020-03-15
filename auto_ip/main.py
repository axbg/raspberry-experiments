import os

from dotenv import load_dotenv
from requests import get
from selenium import webdriver

import providers

load_dotenv(".env")
driver = webdriver.Chrome()
ip = get('https://api.ipify.org').text

index = 0
try:
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
