'''
이 check_post는 크롤링하고자 하는 게시판에 새로운 게시물이
'''

from bs4 import BeautifulSoup
import bs4
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_NOT_REFRESHED = -1


def _get_soup():
    status = 0
    while True: #가끔 서버 상황이 안좋아서 커넥션 에러가 나는 경우를 방지하기 위해 while로 계속 시도
        try:
            req = requests.get('https://www.ajou.ac.kr/kr/ajou/notice.do', verify=False)
            status = 1
        except requests.exceptions.ConnectionError as e:
            print(e)
        finally:
            if status == 1:
                break
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def refresh(currentNumber: int):
    # 새 게시글의 번호 검색 -> page_number
    __soup = _get_soup()
    page_number = __soup.findAll('td', {'class': 'b-num-box'})
    post_order: int = 0
    for index in page_number:
        index: bs4.Tag
        index = index.text.replace('\n', '')
        index = index.replace('\t', '')
        index = index.replace('\r', '')
        index = index.replace(r"'", '')
        try:
            page_number = int(index)
            break
        except ValueError:
            post_order += 1
            pass

    # 새로운 게시물이 올라왔다면
    try:
        if page_number > currentNumber:
            url: bs4.Tag = __soup.findAll('div', {'class': 'b-title-box'})[post_order].find('a')['href']
            url = 'https://www.ajou.ac.kr/kr/ajou/notice.do' + url
            return Refresh(url, page_number)
    except TypeError:
        return None

    else:
        return None


class Refresh():

    def __init__(self, url, number):
        self.url = url
        self.page_number = number
        Refresh.page_number = number
