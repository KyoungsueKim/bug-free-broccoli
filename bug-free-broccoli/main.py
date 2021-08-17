from packages import uData

post01 = uData.init('https://www.ajou.ac.kr/kr/ajou/notice.do?mode=view&articleNo=112441&article.offset=0&articleLimit=10',
                    title=True, text=True)
print(post01.contents)