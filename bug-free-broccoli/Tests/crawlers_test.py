import os
import sys
import pyshorteners as ps

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from packages import uData
import unittest

class CrawlersTest(unittest.TestCase):
    def test_ajounitice(self):
        contents = uData.Content(type=uData.uType.AJOUNOTICE, debug=True)
        print(contents.getpost()) #json 타입으로 반환. 만약 새 게시물이 없으면 None 반환
        pass

    # def test_justtest(self):
    #     s = ps.Shortener(api_key='ce7c70969518275c685266d6be92a05dd398ba66')
    #     url = s.bitly.short('https://www.ajou.ac.kr/kr/ajou/notice.do?mode=list&article.offset=0')

if __name__ == '__main__':
    unittest.main()
    pass