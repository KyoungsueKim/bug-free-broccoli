from PyQt5 import QtCore, QtWidgets, QtTest
from dialog import Ui_Dialog
from packages import uData
import pyautogui
import clipboard
import platform


class MainWindow(Ui_Dialog):

    # PyQt Initializer Method
    def setupUi(self, dialog):
        super(MainWindow, self).setupUi(dialog)
        self.label_currPostNum.setText(str(uData.Refresh.page_number))
        self.pushButton_loadPost.clicked.connect(self.btn_loadPost)
        self.pushButton_checkBoard.clicked.connect(self.btn_checkBoard)
        self.pushButton_sendToKakao.clicked.connect(self.btn_sendKakao)
        self.pushButton_pauseTimer.clicked.connect(self.pauseTimer)

        # BoardCheckTimer
        self.timer = QtCore.QTimer()
        self.timer.start()
        self.timer.setInterval(self.spinBox_updateCycle.value() * 1000)
        self.timer.timeout.connect(self.checkBoardAndSendKakao)

        #Normal Timer at 1ms Interval
        self.loopTimer = QtCore.QTimer()
        self.loopTimer.start()
        self.loopTimer.timeout.connect(self.loop)

        self.spinBox_updateCycle.valueChanged.connect(self.resetBoardCheckTimer)

        print("initialized!")

    #called every 1ms
    def loop(self):
        self.checkPos()
        self.label_updatedTime.setText(str(int(self.timer.remainingTime() / 1000)))


    def btn_loadPost(self):
        url = self.lineEdit_URL.text()
        # option
        text = self.checkBox_text.isChecked()
        title = self.checkBox_title.isChecked()
        dept = self.checkBox_dept.isChecked()
        writer = self.checkBox_writer.isChecked()
        date = self.checkBox_date.isChecked()
        views = self.checkBox_views.isChecked()

        post01 = uData.init(url, text=text, title=title, dept=dept, writer=writer, date=date, views=views)
        self.textBrowser_postView.setText(post01.contents)

    def btn_checkBoard(self):
        check: uData.update.Refresh = uData.refresh()
        if check is not None:
            self.label_currPostNum.setText(str(check.page_number))
            self.lineEdit_URL.setText(check.url)
            self.btn_loadPost()

    def btn_sendKakao(self):
        kakao_textPos_x = self.spinBox_kakaoXpos.value()
        kakao_textPos_y = self.spinBox_kakaoYpos.value()
        if kakao_textPos_x and kakao_textPos_y is not None:
            clipboard.copy(self.textBrowser_postView.toPlainText())
            pyautogui.moveTo(kakao_textPos_x, kakao_textPos_y)
            pyautogui.click()
            QtTest.QTest.qWait(100)

            ctrl = 'ctrl' if platform.system() == 'Windows' else 'command'
            pyautogui.hotkey(ctrl, 'v')
            QtTest.QTest.qWait(1000)
            pyautogui.press('Enter')

        self.resetBoardCheckTimer()

    def checkPos(self):
        self.label_mouseXpos.setText(str(pyautogui.position().x))
        self.label_mouseYpos.setText(str(pyautogui.position().y))

    def resetBoardCheckTimer(self):
        self.timer.setInterval(self.spinBox_updateCycle.value() * 1000)
        self.timer.stop()
        self.timer.start()

    def checkBoardAndSendKakao(self):
        currentPageNumber = int(self.label_currPostNum.text())
        self.btn_checkBoard()
        if uData.Refresh.page_number != currentPageNumber:
            self.btn_sendKakao()

    def pauseTimer(self):
        None

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MainWindow()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
