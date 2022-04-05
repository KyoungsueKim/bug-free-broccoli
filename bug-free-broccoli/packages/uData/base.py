import requests
from bs4 import BeautifulSoup

class BaseContent:
    def __init__(self):
        pass

    def _get_soup(url: str):
        response = requests.get(url, verify=False)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        return soup