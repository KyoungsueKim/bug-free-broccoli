import sys

from PyQt5.QtWidgets import *
#    ui 파일을 불러오기 위한 패키지
from PyQt5 import uic

#    form_class에 ui 파일을 로드한다.
form_class = uic.loadUiType("untitled.ui")[0]


#    윈도우 클래스를 정의할 때 인자로 ui 파일인 form_class를 전달한다.
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_clicked)



    def accept(self):
        print("Press ACCEPT")

    def reject(self):
        print("Press Reject")

    def btn_clicked(self):
        print("Press Button")
        self.textEdit.setText("Press Button")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()