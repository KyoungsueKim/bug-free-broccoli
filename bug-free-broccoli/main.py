from PyQt5 import QtCore, QtWidgets
from main_dialog import Ui_Dialog
from packages import uData
import btn_action
'''
bug-free-broccoli 프로젝트의 시작점이자 메인 코드입니다. 잘 오셨습니다. 환영합니다. 
'''

class MainWindow(Ui_Dialog):
    def setupUi(self, dialog):
        '''
        main_dialog.py의 Ui_Dialog에 있는 컴포넌트들을 그대로 상속받아 각각에 btn_action에서 정의된 기능들을 연결합니다.
        이렇게 하면 xml 형태로 되어있는 main_dialog.ui 파일을 복잡하게 불러올 필요 없이 UI 컴포넌트를 파이썬 코드로서 접근할 수 있으며,
        무엇보다 IDE의 code intelligence 기능과 디버깅 기능을 활용할 수 있습니다.

        :param dialog: 새로이 생성된 QtWidgets.QDialog() -> main.py 실행 시 자동으로 생성됨.
        :return:
        '''
        super(MainWindow, self).setupUi(dialog) # main_dialog.py 상에 정의되어있는 컴포넌트들을 생성해줌.
        self.pushButton_loadPost.clicked.connect(lambda: btn_action.loadPost(self)) # self를 파라메터로 넘겨주어야하기 때문에 lambda를 사용함.
        self.pushButton_checkBoard.clicked.connect(lambda: btn_action.checkBoard(self))
        self.pushButton_sendToKakaoDebug.clicked.connect(lambda: btn_action.sendTextToKakao(self))
        self.pushButton_pauseTimer.clicked.connect(lambda: btn_action.pauseTimer(self))
        self.pushButton_openImagePath.clicked.connect(lambda: btn_action.openImagePath(self))
        self.pushButton_sendImageToKakaoDebug.clicked.connect(lambda: btn_action.sendImageToKakao(self))
        self.spinBox_updateCycle.valueChanged.connect(lambda: btn_action.resetBoardCheckTimer(self))

        '''
        공지사항 게시판 체크를 위한 QtCore.QTimer 입니다. 
        main_dialog 상에 입력된 새로고침 시간이 지날 경우 btn_action.sendNotification(self)를 실행합니다. (기본값 60초)
        '''
        # BoardCheckTimer
        self.timer = QtCore.QTimer()
        self.timer.start()
        self.timer.setInterval(self.spinBox_updateCycle.value() * 1000)
        self.timer.timeout.connect(lambda: btn_action.sendNotification(self))

        '''
        마우스 좌표 체크를 위한 QtCore.QTimer 입니다.
        기본값인 1ms 마다 self.loop 메소드를 실행합니다.
        '''
        # Normal Timer (1ms Interval)
        self.loopTimer = QtCore.QTimer()
        self.loopTimer.start()
        self.loopTimer.timeout.connect(self.loop)

        print("initialized!") # for debugging

    '''
    self.loopTimer에 의해 1ms마다 한 번씩 실행됩니다. 본 메소드는 다음과 같은 작업을 진행합니다. 
    
    1. 마우스 좌표를 1ms마다 체크함. -> btn_action.checkPos
    2. 다음 게시글 체크 시간까지 남은 시간을 GUI상에 표시함. -> self.label_updatedTime.setText
    '''
    # called every 1ms
    def loop(self):
        btn_action.checkPos(self)
        self.label_updatedTime.setText(str(int(self.timer.remainingTime() / 1000)))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog() # Dialog windows의 가장 베이스가 되는 클래스입니다. 이 위에 필요한 GUI 컴포넌트들을 쌓을 수 있습니다. 자세한건 레퍼런스 참조..
    MainWindow().setupUi(Dialog) # 위에서 미리 정의해둔 UI 컴포넌트들을 Dialog에 쌓습니다.
    Dialog.show() # 쌓인 다이얼로그를 화면에 띄웁니다.
    sys.exit(app.exec_())
