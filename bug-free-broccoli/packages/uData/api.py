"""
uData.api
~~~~~~~~~

이 uData.api 모듈은 아주대학교 공지사항 게시판에 올라와있는 게시물을
입맛대로 다룰 때 필요한 메소드들을 편리하게 제공합니다.
"""

from . import contents, update

def init(url: str, text: bool = True, title: bool = False, dept: bool = False, writer: bool = False,
         date: bool = False, views: bool = False):
    '''
    게시물의 내용을 담을 때 사용되는 Content 객체를 초기화하기 위한 메소드입니다. Content 관련 메소드를 실행하기 전 가장 먼저 실행되어야합니다.

    :param url: (str) 아주대학교 게시물의 url입니다.
    :param text: (bool) 게시글 <내용>을 포함시킬지 여부입니다.
    :param title: (bool) 게시글 <제목>을 포함시킬지 여부입니다.
    :param dept: (bool) 게시글 <작성부서>를 포함시킬지 여부입니다.
    :param writer: (bool) 게시글 <작성자>를 포함시킬지 여부입니다.
    :param date: (bool) 게시글 <날짜>를 포함시킬지 여부입니다.
    :param views: (bool) 게시글 <조회수>를 포함시킬지 여부입니다.
    :return: (uData.contents.Content)
    '''
    return contents.Content(url, text, title, dept, writer, date, views)
