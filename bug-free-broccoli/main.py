from packages import uData
import re

post02 = uData.init('https://www.ajou.ac.kr/kr/ajou/notice.do?mode=view&articleNo=112441&article.offset=0&articleLimit=10', title=True, text=True)
print(post02.contents)

# p = re.compile(r'"https://.+?"')
#
# string01 = r'<p style="text-align: center;"><span style="color: rgb(226, 80, 65);"><a href="https://hub.ajou.ac.kr/ncrProgramAppl/a/m/getProgramDetail.do?npiKeyId=NCR000000000140"><em><u>기초 입사지원 서류 작성법 특강 신청바로가기</u></em></a></span></p>'
# m = p.search(string01)
# if m:
#     print(m.group())