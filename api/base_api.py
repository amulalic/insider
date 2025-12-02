import requests
from config.config import Config


class BaseAPI:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.timeout = Config.TIMEOUT
        self.headers = Config.HEADERS
        self.session = requests.Session()

    def get(self, endpoint, params=None, **kwargs):
        """Generic GET request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(
            url,
            params=params,
            timeout=kwargs.get("timeout", self.timeout),
            headers=kwargs.get("headers", self.headers),
        )
        return response

    def post(self, endpoint, data=None, json=None, **kwargs):
        """Generic POST request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(
            url,
            data=data,
            json=json,
            timeout=kwargs.get("timeout", self.timeout),
            headers=kwargs.get("headers", self.headers),
        )
        return response

    def put(self, endpoint, data=None, json=None, **kwargs):
        """Generic PUT request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(
            url,
            data=data,
            json=json,
            timeout=kwargs.get("timeout", self.timeout),
            headers=kwargs.get("headers", self.headers),
        )
        return response

    def delete(self, endpoint, **kwargs):
        """Generic DELETE request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(
            url,
            timeout=kwargs.get("timeout", self.timeout),
            headers=kwargs.get("headers", self.headers),
        )
        return response

    def close(self):
        """Close the session"""
        self.session.close()
