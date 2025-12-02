"""Configuration management for API tests"""


class Config:
    BASE_URL = "https://petstore.swagger.io/v2"
    TIMEOUT = 10
    HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
