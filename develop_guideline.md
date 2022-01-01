# Develop Guideline
--------------------
## 프로그램 GUI 수정
<img width="351" alt="image" src="https://user-images.githubusercontent.com/61102713/147847784-02bc9139-3a06-4699-b89d-215a74fdd4eb.png">

본 프로그램의 GUI는 Cross-platform GUI 라이브러리인 PyQt5를 이용해 구현되어있습니다. 본 프로그램은 GUI 구현시에 .ui파일을 그대로 불러와 사용하는 방식이 아닌, .ui파일을 .py코드로 변경한 후 이를 새로운 파이썬 코드에서 상속받아 각 컴포넌트에 기능을 연결하는 방식으로 구현되어있습니다. 
이렇게 하면 xml 형태로 되어있는 .ui 파일을 복잡하게 불러올 필요 없이 UI 컴포넌트를 파이썬 코드로서 접근할 수 있으며, 무엇보다 IDE의 code intelligence 기능과 디버깅 기능을 활용할 수 있습니다. 본 프로그램에 구현되어있는 GUI를 조금 더 쉽고 편하게 수정할 수 있는 방법을 다음과 같이 안내해드립니다.

### 1. QtCreator(QtDesigner)을 이용해 Dialog 디자인
<img width="1680" alt="image" src="https://user-images.githubusercontent.com/61102713/147847875-b6e6b544-a1a6-4a27-8f22-f7097f4d85f8.png">

위 그림과 같이 QtCreator에서 수정하고 싶은 dialog의 ui 파일을 불러와 수정한 뒤 파일을 .ui로 저장합니다. QtCreator의 자세한 사용 방법은 레퍼런스를 직접 참고해보세요. 

### 2. .ui 파일을 .py 파일로 변환
```Shell
pyuic5 -x <.ui파일명> -o <.py파일명>
```
위 코드를 이용하시면 손쉽게 .ui파일을 .py파일로 변경하실 수 있습니다. 다음은 main_dialog.ui를 main_dialog.py로 변경하는 코드 예시입니다. 

```Shell
pyuic5 -x main_dialog.ui -o main_dialog.py
```

### 3. 새로운 파이썬 파일에서 변환된 .py 파일을 상속받아 사용
새로운 파이썬 파일을 생성하고 다음과 같은 코드를 이용해 새로운 MainWindow 클래스에서 .py로 변경된 dialog 코드를 상속받아 각 컴포넌트에 기능을 얹어줍니다. 이렇게 하면 .ui파일을 .py로 변경할 때 이전에 작성한 기능 관련 코드가 날라가는걸 방지할 수 있습니다. 
```Python
from <변환된 .py 파일명> import Ui_Dialog

class MainWindow(Ui_Dialog): # 새로운 Dialog 클래스. 이름은 꼭 MainWindow일 필요는 없다. 
    def setupUi(self, dialog):
        super(MainWindow, self).setupUi(dialog) # MainWindow 클래스의 부모 클래스인 <.py 파일명>의 Ui_Dialog 클래스 상에 정의되어있는 컴포넌트들을 생성해줌.
        # 필요한 기능은 다음과 같이 연결해줄 수 있다.
        self.pushButton.clicked.connect(lambda: <원하는 메소드 이름>(self)) # self를 파라메터로 넘겨주어야하기 때문에 lambda를 사용함.

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog() # Dialog windows의 가장 베이스가 되는 클래스. 이 위에 필요한 GUI 컴포넌트들을 쌓을 수 있음. 자세한건 레퍼런스 참조..
    MainWindow().setupUi(Dialog) # 위에서 미리 정의해둔 UI 컴포넌트들을 Dialog에 쌓는다.
    Dialog.show() # 쌓인 다이얼로그를 화면에 띄운다.
    sys.exit(app.exec_())
```

본 방식은 main.py를 작성할 때도 적용되었습니다. main_dialog.ui를 QtCreator에서 디자인 한 후 이를 .py 코드로 변환시켜 main.py에서 해당 코드를 상속받아 기능을 연결하는 구조입니다. 참고해보시길 바랍니다. 