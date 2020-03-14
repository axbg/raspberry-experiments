class AbstractProvider:
    name = None
    url = None

    @staticmethod
    def scrap(driver, username, password, domain, ip):
        pass

    @classmethod
    def get_implementation(cls, provider_name):
        for clz in cls.__subclasses__():
            if clz.__name__.lower() == str(provider_name).lower():
                return clz
