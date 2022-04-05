"""
이 uData.api는 uData의 기능들을 보다 직관적으로 사용할 수 있도록 하는 메소드들을 제공합니다.
"""

from packages.obsolate import contents


def init(url: str, text: bool = True, title: bool = False, dept: bool = False, writer: bool = False,
         date: bool = False, views: bool = False):
    '''
    게시물의 내용이 담기는 Content 객체를 생성하기 위한 메소드입니다.

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
