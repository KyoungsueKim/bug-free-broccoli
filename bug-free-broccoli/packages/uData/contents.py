"""
uData.contents
~~~~~~~~~~~~~~

이 uData.contents 모듈은 Contents 객체를 관리하는 모듈입니다.
"""
import bs4.element
import requests
from bs4 import BeautifulSoup
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _get_soup(url: str):
    response = requests.get(url, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup


# TODO b-title 말고 b-cate(게시글 종류)도 추출 가능하도록 get_메서드 하나 더 만들기.
def _get_title(soup: BeautifulSoup):
    title: bs4.ResultSet = soup.select_one('div.b-top-box')
    title = title.select('div.b-top-box > p > span')

    span_title = 1
    title: bs4.Tag = title[span_title]

    result = title.get_text()
    return result


def _get_dept(soup: BeautifulSoup):
    dept: bs4.ResultSet = soup.select_one('div.b-info-box')
    dept = soup.select('ul > li > span')

    span_dept = 0
    dept: bs4.Tag = dept[span_dept]

    result = dept.get_text()
    return result


def _get_writer(soup: BeautifulSoup):
    writer: bs4.ResultSet = soup.select_one('div.b-info-box')
    writer = writer.select('ul > li > span')

    span_writer = 1
    writer: bs4.Tag = writer[span_writer]

    result = writer.get_text()
    return result


def _get_date(soup: BeautifulSoup):
    date: bs4.ResultSet = soup.select_one('div.b-info-box')
    date = date.select('ul > li > span')

    span_date = 3
    date: bs4.Tag = date[span_date]

    result = date.get_text()
    return result


def _get_views(soup: BeautifulSoup):
    views: bs4.ResultSet = soup.select_one('div.b-info-box')
    views = views.select('ul > li > span')

    span_views = 5
    views: bs4.Tag = views[span_views]

    result = views.get_text()
    return result


def _get_text(soup: BeautifulSoup):
    result = ''
    text: bs4.Tag = soup.find("div", {"class": "fr-view"})

    text: bs4.ResultSet = text.find_all("p")

    p1 = re.compile(r'"https://.+?"')
    p2 = re.compile(r'"http://.+?"')
    for list in text:
        m1 = p1.search(str(list))
        m2 = p2.search(str(list))
        if m1 or m2: #링크가 있을 경우
            m = m1 if m1 is not None else m2
            result += re.sub('<.+?>', '', str(list), 0)
            url = '(' + m.group() + ')'
            url = re.sub('amp;', '', url)
            result += url
            result += '\n'
        else:
            result += re.sub('<.+?>', '', str(list), 0)
            result += '\n'
    return result


class Content:
    def __init__(self, url: str, text: bool = True, title: bool = False, dept: bool = False, writer: bool = False,
                 date: bool = False, views: bool = False):
        self.__url = url
        self.__isText = text
        self.__isTitle = title
        self.__isDept = dept
        self.__isWriter = writer
        self.__isDate = date
        self.__isViews = views

    @property
    def contents(self):
        '''
        uData.init()를 통해 지정된 옵션에 따라 게시글 내용을 반환합니다.
        '''

        contents: str = ''
        soup = _get_soup(self.__url)

        if self.__isTitle:
            contents += f'[제목]\n {_get_title(soup)} \n'

        if self.__isDept:
            contents += f'[부서]\n {_get_dept(soup)} \n'

        if self.__isWriter:
            contents += f'[작성자]\n {_get_writer(soup)} \n'

        if self.__isDate:
            contents += f'[작성일]\n {_get_date(soup)} \n'

        if self.__isViews:
            contents += f'[조회수]\n {_get_views(soup)} \n'

        if self.__isText:
            contents += f'[본문]\n {_get_text(soup)} \n'

        return contents