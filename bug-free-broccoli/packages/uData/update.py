from bs4 import BeautifulSoup
import requests
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_NOT_REFRESHED = -1

def _get_soup():
    req = requests.get('https://www.ajou.ac.kr/kr/ajou/notice.do', verify=False)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def refresh(currentNumber: int):
    #새 게시글의 번호 검색 -> page_number
    __soup = _get_soup()
    page_number = __soup.find('td', {'class': 'b-num-box'}).text
    page_number = page_number.replace('\n', '')
    page_number = page_number.replace('\t', '')
    page_number = page_number.replace('\r', '')
    page_number = page_number.replace(r"'", '')
    page_number = int(page_number)

    #새로운 게시물이 올라왔다면
    if page_number > currentNumber:

        url = __soup.find('div', {'class': 'b-title-box'})
        url = str(url)
        url = re.findall(r'<a href="(.*?)"', url)
        url = str(url)
        url = url.replace('amp;', '')
        url = url.replace("['", '')
        url = url.replace("']", '')
        url = 'https://www.ajou.ac.kr/kr/ajou/notice.do' + url

        return Refresh(url, page_number)

    else:
        return None

class Refresh():

    def __init__(self, url, number):
        self.url = url
        self.page_number = number
        Refresh.page_number = number
