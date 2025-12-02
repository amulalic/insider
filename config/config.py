"""Configuration management for API tests"""


class ConfigApi:
    BASE_URL = "https://petstore.swagger.io/v2"
    TIMEOUT = 10
    HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


class ConfigUI:
    BASE_URL = "https://useinsider.com/"
    QA_CAREERS_URL = "https://useinsider.com/careers/quality-assurance/"
