from providers.abstract_provider import AbstractProvider


class NameCheap(AbstractProvider):
    name = "namecheap"
    url = "https://namecheap.com"
    logged_in = False

    @staticmethod
    def login(driver, username, password):
        driver.get("https://www.namecheap.com/myaccount/login/")

        username_input = driver.find_elements_by_class_name("nc_username_required")[0]
        password_input = driver.find_elements_by_class_name("nc_password")[0]
        login_button = driver.find_element_by_id(
            "ctl00_ctl00_ctl00_ctl00_base_content_web_base_content_home_content_page_content_left_ctl02_LoginButton")

        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        NameCheap.logged_in = True

    @staticmethod
    def scrap(driver, username, password, domain, ip):
        if not NameCheap.logged_in:
            NameCheap.login(driver, username, password)

        driver.get("https://ap.www.namecheap.com/Domains/DomainControlPanel/" + domain + "/advancedns")

        value_td = NameCheap.wait_element(lambda x: x.find_elements_by_class_name("value")[1], driver)
        value_p = value_td.find_elements_by_tag_name("p")[0]
        value_p.click()

        value_input = driver.find_element_by_xpath("//input[contains(@name,'idAddress')]")
        value_input.clear()
        value_input.send_keys(ip)

        save_input = driver.find_elements_by_class_name("save")[1]
        save_input.click()
