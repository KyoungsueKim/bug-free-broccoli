from PyQt5 import QtCore, QtWidgets
from dialog import Ui_Dialog
from packages import uData
import btnaction as btn

class MainWindow(Ui_Dialog):


    def setupUi(self, dialog):
        super(MainWindow, self).setupUi(dialog)
        self.pushButton_loadPost.clicked.connect(lambda: btn.loadPost(self))
        self.pushButton_checkBoard.clicked.connect(lambda: btn.checkBoard(self))
        self.pushButton_sendToKakaoDebug.clicked.connect(lambda: btn.sendTextToKakao(self))
        self.pushButton_pauseTimer.clicked.connect(lambda: btn.pauseTimer(self))
        self.pushButton_openImagePath.clicked.connect(lambda: btn.openImagePath(self))
        self.pushButton_sendImageToKakaoDebug.clicked.connect(lambda: btn.sendImageToKakao(self))

        # BoardCheckTimer
        self.timer = QtCore.QTimer()
        self.timer.start()
        self.timer.setInterval(self.spinBox_updateCycle.value() * 1000)
        self.timer.timeout.connect(lambda: btn.sendNotification(self))

        #Normal Timer (1ms Interval)
        self.loopTimer = QtCore.QTimer()
        self.loopTimer.start()
        self.loopTimer.timeout.connect(self.loop)

        self.spinBox_updateCycle.valueChanged.connect(lambda: btn.resetBoardCheckTimer(self))

        print("initialized!")

    #called every 1ms
    def loop(self):
        btn.checkPos(self)
        self.label_updatedTime.setText(str(int(self.timer.remainingTime() / 1000)))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MainWindow()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
