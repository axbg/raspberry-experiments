from providers.abstract_provider import AbstractProvider


class NameCheap(AbstractProvider):
    name = "namecheap"
    url = "https://namecheap.com"

    @staticmethod
    def scrap(driver, username, password, domain, ip):
        driver.get("https://www.namecheap.com/myaccount/login/")

        username_input = driver.find_elements_by_class_name("nc_username_required")[0]
        password_input = driver.find_elements_by_class_name("nc_password")[0]
        login_button = driver.find_element_by_id(
            "ctl00_ctl00_ctl00_ctl00_base_content_web_base_content_home_content_page_content_left_ctl02_LoginButton")

        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        selected_domain = NameCheap.wait_element(lambda x: x.find_element_by_xpath(
            "//a[contains(@href,'/domains/domaincontrolpanel/" + domain + "/domain')]"), driver)
        selected_domain.click()

        driver.find_element_by_xpath(
            "//a[contains(@href,'/Domains/DomainControlPanel/" + domain + "/advancedns')]").click()

        allow_cookies_btn = NameCheap.wait_element(lambda x: x.find_elements_by_class_name("accept-cookies-button"),
                                                   driver)[0]
        allow_cookies_btn.click()

        value_td = driver.find_elements_by_class_name("value")[1]
        value_p = value_td.find_elements_by_tag_name("p")[0]
        value_p.click()

        value_input = driver.find_element_by_xpath("//input[contains(@name,'idAddress')]")
        value_input.clear()
        value_input.send_keys(ip)

        save_input = driver.find_elements_by_class_name("save")[1]
        save_input.click()
