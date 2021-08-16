import json
from bs4.element import ResultSet
import requests
from bs4 import BeautifulSoup
import re
import json
import urllib3 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import urllib.request
    
def PrintTitle(result): #제목 형식에 맞게 출력
    print("[제목]\n {}".format(result))
    print()

def PrintDepartment(result): #제목 형식에 맞게 출력
    print("[부서]\n {}".format(result))
    print()

def PrintWriter(result): #제목 형식에 맞게 출력
    print("[작성자]\n {}".format(result))
    print()

def PrintWritedDay(result):
    print("[작성일]\n {}".format(result))
    print()

def PrintAOV(result): #제목 형식에 맞게 출력
    print("[조회수]\n {}".format(result))
    print()

def PrintTOC(result): #본문 형식에 맞게 출력
    print("[본문]\n {}".format(result))
    print()

def PrintAll(post): ##전부 출력
    PrintTitle(post.GetTitle())
    PrintDepartment(post.GetDepartment())
    PrintWriter(post.GetWriter())
    PrintWritedDay(post.GetWritedDate())
    PrintAOV(post.GetAmountOfViewer())
    PrintTOC(post.GetText())

def GetSoup(url): #URL 입력하면 html을 parsing해서 반환하는 함수
    response  = requests.get(url, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup

class TotalData :
    #클래스 생성자 : URL
    def __init__(self, url):
        self.url = url

    def GetTitle(self):  #제목
        title = GetSoup(self.url)
        title = title.select_one('div.b-top-box')
        title = title.select('div.b-top-box > p > span')      
        De = title[1]
        result = De.get_text()
        return result

    def GetDepartment(self):  #작성 부서
        department = GetSoup(self.url)
        department = department.select_one('div.b-info-box')
        department = department.select('ul > li > span')      
        De = department[0]
        result = De.get_text()
        return result

    def GetWriter(self):  #작성자
        writer = GetSoup(self.url)
        writer = writer.select_one('div.b-info-box')
        writer = writer.select('ul > li > span')      
        De = writer[1]
        result = De.get_text()
        return result

    def GetWritedDate(self):  #작성일
        writed_date = GetSoup(self.url)
        writed_date = writed_date.select_one('div.b-info-box')
        writed_date = writed_date.select('ul > li > span')      
        De = writed_date[3]
        result = De.get_text()
        return result

    def GetAmountOfViewer(self):  #조회수
        amount_of_viewer = GetSoup(self.url)
        amount_of_viewer = amount_of_viewer.select_one('div.b-info-box')
        amount_of_viewer = amount_of_viewer.select('ul > li > span')      
        De = amount_of_viewer[5]
        result = De.get_text()
        return result

    """
        추가해야 할 기능 : 하이퍼링크가 포함된 문장은 따로 하이퍼링크를 찾아서 문자열에 추가해야 함.
        (예 : '수강신청 바로가기' --> '수강신청 바로가기(http://~~))
    """
    def GetText(self):  #텍스트
        text_contents = GetSoup(self.url)
        text_contents = text_contents.find("div",{"class":"fr-view"})
        text_contents = str(text_contents)
        text_contents = text_contents.replace("</p>",'\n')
        text_contents = re.sub('<.+?>', '', text_contents, 0)
        result = text_contents
        # k = ""
        # for i in range(len(text_contents)): #와 무친 이게 되네;;
        #     k += text_contents[i].get_text()
        # return k
        return result

    def GetImage(self):  #이미지 파일
        image = GetSoup(self.url)
        image = image.find_all("title")
        image = str(image) 
        image = image.replace('</title>', '')
        image = image.replace('<title>', '')
        return image
    
    def GetAttached(self):  #첨부파일
        attached = GetSoup(self.url)
        attached = attached.find_all("title")
        attached = str(attached)
        attached = attached.replace('</title>', '')
        attached = attached.replace('<title>', '')
        return attached    


if __name__ == '__main__':
    post_01 = TotalData(
        "https://www.ajou.ac.kr/kr/ajou/notice.do?mode=view&articleNo=112368&article.offset=0&articleLimit=10")
    PrintAll(post_01)
    post_01.GetTitle()
    print('HelloWorld')

