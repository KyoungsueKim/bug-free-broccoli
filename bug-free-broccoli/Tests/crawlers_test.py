import os
import sys
import pyshorteners as ps

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from packages import uData
import unittest

class CrawlersTest(unittest.TestCase):
    def test_ajounitice(self):
        contents = uData.Content(type=uData.uType.AJOUNOTICE)
        contents2 = uData.Content(url='https://www.ajou.ac.kr/kr/ajou/notice.do?mode=view&articleNo=179211')
        # json 타입으로 반환. 만약 새 게시물이 없으면 None 반환
        # 다음과 같이 .으로 내용 접근 가능하게 ..
        print(contents.getpost().text)
        pass

    def test_badcase(self):
        # 다음과 같이 type과 url 모두 파라메터가 넘겨질 경우 처리는 url 먼저
        contents = uData.Content(type=uData.uType.AJOUNOTICE, url='https://www.ajou.ac.kr/kr/ajou/notice.do?articleNo=179211')
        pass

if __name__ == '__main__':
    unittest.main()
    pass