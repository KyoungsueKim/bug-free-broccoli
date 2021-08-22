from bs4 import BeautifulSoup
import requests
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__NOT_REFREASHED = -1
page_number = __NOT_REFREASHED

def _get_soup():
    req = requests.get('https://www.ajou.ac.kr/kr/ajou/notice.do', verify=False)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def refreash():

    #새 게시글의 번호 검색 -> latest
    __soup = _get_soup()
    latest = __soup.find('td', {'class': 'b-num-box'}).text
    latest = latest.replace('\n', '')
    latest = latest.replace('\t', '')
    latest = latest.replace('\r', '')
    latest = latest.replace(r"'", '')
    latest = int(latest)

    #새로운 게시물이 올라왔다면
    if latest > page_number:
        url = __soup.find('div', {'class': 'b-title-box'})
        url = str(url)
        url = re.findall(r'<a href="(.*?)"', url)
        url = str(url)
        url = url.replace('amp;', '')
        url = url.replace("['", '')
        url = url.replace("']", '')
        url = 'https://www.ajou.ac.kr/kr/ajou/notice.do' + url

        return Refreash(url, latest)

    else:
        return None

class Refreash():
    def __init__(self, url, page_number):
        self.url = url
        self.page_number = page_number