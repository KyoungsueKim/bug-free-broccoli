'''
utype은 uData.Content 객체 생성시에 정해줘야하는 크롤러 종류를 enum 형식으로 제공합니다.
uType.AJOUNOTICE 와 같이 사용하시면 됩니다.
'''

import enum
from enum import Enum

class uType(Enum):
    AJOUNOTICE = 'ajounotice' # 아주대학교 공지사항 게시판 (https://www.ajou.ac.kr/kr/ajou/notice.do)