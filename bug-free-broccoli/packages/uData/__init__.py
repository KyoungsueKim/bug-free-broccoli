'''
uData 모듈은 크롤링하고자 하는 게시판을 지정하여 최신 게시물을 json 타입으로 가져올 수 있습니다.
게시글에 이미지가 같이 포함되어있는 경우 bug-free-broccoli/images 폴더에 이미지가 같이 저장됩니다.
'''

from .utype import uType

class Content():
    def __init__(self, **kwargs):
        '''
        알맞는 종류의 크롤러 인스턴스를 생성해주기 위한 일종의 설정 마법사 클래스입니다.

        Keyword Args:
            type (uData.uType): 크롤러 타입을 명시해줄 수 있습니다.
            url (str): 크롤링을 원하는 특정 게시물을 지정해주고 싶을 때 url을 입력합니다. url이 입력된 경우 type 파라메터는 무시됩니다.

        Raises:
            ValueError: type 파라메터의 속성이 uType과 불일치할 때 일어납니다.
        '''

        if kwargs['type'] != (uType or None): # type 파라메터의 속성이 uType이 아니라면
            raise ValueError('invaild type for' + str())

        self.kwargs = kwargs
        self.kwargs["type"] = kwargs.pop("type", None)
        self.kwargs["url"] = kwargs.pop("url", None)


        pass



