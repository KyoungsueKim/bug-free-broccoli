from bs4 import BeautifulSoup
import bs4
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_NOT_REFRESHED = -1

# 크롤링을 건너뛸 키워드 Set
SKIP_KEYWORDS = {
    '예비군',
    # 필요시 여기에 더 많은 키워드를 추가할 수 있습니다
    # '동원훈련',
    # '민방위',
}


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
            # 게시물 제목과 URL을 가져옴
            title_box = __soup.findAll('div', {'class': 'b-title-box'})[post_order]
            title_text = title_box.find('a').text.strip()
            
            # 제목에 건너뛸 키워드가 포함되어 있는지 확인
            for keyword in SKIP_KEYWORDS:
                if keyword in title_text:
                    print(f"'{keyword}' 관련 게시물 건너뛰기: {title_text}")
                    return None
                
            url: bs4.Tag = title_box.find('a')['href']
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
