from packages import uData

post02 = uData.init('https://www.ajou.ac.kr/kr/ajou/notice.do?mode=view&articleNo=112441&article.offset=0&articleLimit=10', title=True, text=True)
print(post02.contents)