'''
uData 모듈은 크롤링하고자 하는 게시판을 지정하여 최신 게시물을 json 타입으로 가져올 수 있습니다.
게시글에 이미지가 같이 포함되어있는 경우 bug-free-broccoli/images 폴더에 이미지가 같이 저장됩니다.
'''

from .utype import uType

class Content():
    def __init__(self, type: uType, **kwargs):
        '''
        Contents 객체 생성시에 필요한 값들이 유효한지 검증하고 기본 값을 설정해줍니다.

        :param type -> uType: 크롤러 종류입니다. (ex: uType.AJOUNOTICE)
        :param kwargs:
            url -> str: 특정 게시물을 크롤링해올 때 지정하는 url입니다.
        '''
        if type.__class__ != uType: # type 파라메터의 속성이 uType이 맞는지 검사.
            raise ValueError(f'invaild type for {type.__class__}')
        self.type = type
        self.kwargs = kwargs
        self.kwargs["url"] = kwargs.pop("url", None)
        pass

