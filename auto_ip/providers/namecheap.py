from providers.abstract_provider import AbstractProvider


class NameCheap(AbstractProvider):
    name = "namecheap"
    url = "https://namecheap.com"

    @staticmethod
    def scrap(driver, username, password, domain, ip):
        print(username)
        print(password)
        print(domain)
        print(ip)
