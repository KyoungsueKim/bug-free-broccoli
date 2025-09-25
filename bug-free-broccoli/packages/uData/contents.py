"""
uData.contents
~~~~~~~~~~~~~~

이 uData.contents 모듈은 Contents 객체를 관리하는 모듈입니다.
"""
import os
import ssl
import urllib.request
import warnings

import bs4.element
import requests
from bs4 import BeautifulSoup
import re
import urllib3
import pyshorteners as ps
import apikeyconfig as apikey
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _get_soup(url: str):
    response = requests.get(url, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup


class Content:
    def __init__(self, url: str, text: bool = True, title: bool = False, dept: bool = False, writer: bool = False,
                 date: bool = False, views: bool = False):
        self.url = url
        self.__isText = text
        self.__isTitle = title
        self.__isDept = dept
        self.__isWriter = writer
        self.__isDate = date
        self.__isViews = views
        self.__soup = _get_soup(self.url)

        self.hasImage: bool = False
        self.page_number: int = -1

    # TODO b-title 말고 b-cate(게시글 종류)도 추출 가능하도록 get_메서드 하나 더 만들기.
    @property
    def title(self):
        title: bs4.ResultSet = self.__soup.select_one('div.b-top-box')
        title = title.select('div.b-top-box > p > span')

        span_title = 1
        title: bs4.Tag = title[span_title]

        result = title.get_text()
        return result

    @property
    def dept(self):
        dept: bs4.ResultSet = self.__soup.select_one('div.b-info-box')
        dept = dept.select('ul > li > span')

        span_dept = 0
        dept: bs4.Tag = dept[span_dept]

        result = dept.get_text()
        return result

    @property
    def writer(self):
        writer: bs4.ResultSet = self.__soup.select_one('div.b-info-box')
        writer = writer.select('ul > li > span')

        span_writer = 1
        writer: bs4.Tag = writer[span_writer]

        result = writer.get_text()
        return result

    @property
    def date(self):
        date: bs4.ResultSet = self.__soup.select_one('div.b-info-box')
        date = date.select('ul > li > span')

        span_date = 3
        date: bs4.Tag = date[span_date]

        result = date.get_text()
        return result

    @property
    def views(self):
        views: bs4.ResultSet = self.__soup.select_one('div.b-info-box')
        views = views.select('ul > li > span')

        span_views = 5
        views: bs4.Tag = views[span_views]

        result = views.get_text()
        return result

    # TODO: 이미지 소스 URL은 가져오지 않도록 구별하는 작업 필요.
    @property
    def text(self):
        result = ''
        text: bs4.Tag = self.__soup.find("div", {"class": "fr-view"})

        text: bs4.ResultSet = text.find_all("p")

        # 링크가 걸려있을 경우 텍스트 뒤에 URL을 표시하는 역할
        p1 = re.compile(r'"https://.+?"')
        p2 = re.compile(r'"http://.+?"')
        for element in text:
            m1 = p1.search(str(element))
            m2 = p2.search(str(element))
            if m1 or m2:  # 링크가 있을 경우
                m = m1 if m1 is not None else m2
                result += re.sub('<.+?>', '', str(element), 0)
                url = '(' + m.group() + ')'
                url = re.sub('amp;', '', url)
                # TODO: 텍스트 뒤에 URL 붙이는 기능 비활성화됨. 필요할경우 나중에 다시 활성화할것
                # result += url
                result += '\n'
            else:
                result += re.sub('<.+?>', '', str(element), 0)
                result += '\n'
        return result

    @property
    def contents(self):
        '''
        uData.init()를 통해 지정된 옵션에 따라 게시글 텍스트를 반환합니다.
        '''

        contents: str = ''

        if self.__isTitle:
            contents += f'[제목]: {self.title}) \n'

        # 게시글 url부분
        # if apikey.bitlyAPIkey != 'YOUR API KEY HERE': #api키가 뭐라도 적혀있다면
        #     s = ps.Shortener(api_key=apikey.bitlyAPIkey)
        #     url = s.bitly.short(self.url)
        # else:
        #     url = self.url
        #     warnings.warn('bitlyAPIkey needed! Please type your bitly API KEY into your bug-free-broccoli/apikeyconfig.py')

        url = self.url

        contents += f'{url}\n\n'

        if self.__isDept:
            contents += f'[부서]: {self.dept} \n'

        if self.__isWriter:
            contents += f'[작성자]: {self.writer} \n'

        if self.__isDate:
            contents += f'[작성일]: {self.date} \n'

        if self.__isViews:
            contents += f'[조회수]: {self.views} \n'

        if self.__isText:
            contents += f'\n {self.text} \n'

        return contents

    def saveImage(self):
        """
        해당 Content의 게시글에 이미지들을 저장합니다. 만약 이미지들이 있다면 self.hasIamge가 True가 됩니다.
        """
        text: bs4.Tag = self.__soup.find("div", {"class": "fr-view"})
        text: bs4.ResultSet = text.find_all("p")

        index: int = 0
        result: bool = False
        for element in text:
            element: bs4.Tag = element.select_one('img')
            if element is not None:  # 이미지가 존재한다면
                element = element['src']
                #src에서 뽑아낸 소스에 http로 시작한다면, 즉 도메인 ajou.ac.kr가 있다면
                result = re.compile('http').match(element)
                if result is not None:
                    url = element

                else: #src에서 뽑아낸 소스에 도메인 ajou.ac.kr이 없다면
                    url = 'https://www.ajou.ac.kr' + element

                type = re.compile(r'\.[a-zA-Z]+').findall(element)[-1] #.[a-z]로 시작하는 패턴 중 맨 뒤엣꺼 하나 뽑기. 즉 .jpg나 .png처럼 확장자를 뽑기
                path = os.path.abspath('images')
                os.system(f'curl {url} > {path}/{index}{type}')  # curl 명령어로 이미지 다운로드
                index += 1
                self.hasImage = True


