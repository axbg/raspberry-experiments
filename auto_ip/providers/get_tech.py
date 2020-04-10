from providers.abstract_provider import AbstractProvider


class GetTech(AbstractProvider):
    name = "gettech"
    url = "https://get.tech"
    panel_url = ""
    logged_in = False

    @staticmethod
    def login(driver, domain, username, password):
        driver.get(GetTech.url + "/login")

        username_input = GetTech.wait_element(lambda x: x.find_element_by_name("username"), driver)
        password_input = driver.find_element_by_name("password")
        login_button = driver.find_element_by_xpath("//input[@value='Sign In']")

        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        my_account = GetTech.wait_element(lambda x: x.find_elements_by_class_name("dropdown-toggle")[3], driver)
        my_account.click()

        my_panel = my_account.find_element_by_xpath("//a[@href='cpanel-login']")
        my_panel.click()

        GetTech.wait_element(lambda x: x.find_element_by_xpath("//a[@href='/servlet/ShowFundsSummaryServlet']"), driver)
        driver.get("https://controlpanel.tech/servlet/ListAllOrdersServlet?formaction=listOrders")

        domain_root = domain if domain.count(".") == 1 else domain.split(".", 1)[1]
        my_domain_panel = GetTech.wait_element(lambda x: x.find_element_by_xpath("//a[@title='" + domain_root + "']"),
                                               driver)
        my_domain_panel.click()

        GetTech.panel_url = driver.current_url
        GetTech.logged_in = True

    @staticmethod
    def scrap(driver, username, password, domain, ip):
        if not GetTech.logged_in:
            GetTech.login(driver, domain, username, password)
        else:
            driver.get(GetTech.panel_url)

        dns_management = GetTech.wait_element(lambda x: x.find_element_by_xpath("//span[contains(text(), "
                                                                                "'Manage DNS')]"), driver)
        dns_management.click()

        driver.switch_to.window(driver.window_handles[1])

        my_domain = GetTech.wait_element(lambda x: x.find_element_by_xpath("//a[contains(text(), "
                                                                           "'" + domain + "')]"), driver)
        my_domain.click()

        modify_btn = GetTech.wait_element(lambda x: x.find_element_by_name("btnModRecord"), driver)
        modify_btn.click()

        ip_input = driver.find_element_by_name("IPvalue")
        ip_input.clear()
        ip_input.send_keys(ip)

        save_changes = driver.find_element_by_name("submitform")
        save_changes.click()

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
