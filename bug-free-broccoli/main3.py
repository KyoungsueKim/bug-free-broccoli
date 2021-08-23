from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from untitled import Ui_Dialog
from packages import uData
import pyautogui
import clipboard
import asyncio

class MainWindow(Ui_Dialog):

    def setupUi(self, Dialog):
        super(MainWindow, self).setupUi(Dialog)
        self.label_3.setText(str(uData.update.page_number))
        self.pushButton.clicked.connect(self.btn_clicked)
        self.pushButton_2.clicked.connect(self.btn_clicked_2)
        self.pushButton_3.clicked.connect(self.btn_clicked_3)
        self.timer = QtCore.QTimer()
        self.timer.start()
        self.timer.setInterval(70)
        self.timer.timeout.connect(self.checkPos)
        print("initialized!", self.timer.isActive())

    def btn_clicked(self):
        url = self.textEdit.toPlainText()
        #option
        text = self.checkBox.isChecked()
        title = self.checkBox_2.isChecked()
        dept = self.checkBox_3.isChecked()
        writer = self.checkBox_4.isChecked()
        date = self.checkBox_5.isChecked()
        views = self.checkBox_6.isChecked()

        post01 = uData.init(url, text=text, title=title, dept=dept, writer=writer, date=date, views=views)
        self.textBrowser.setText(post01.contents)

    def btn_clicked_2(self):
        check: uData.update.Refreash = uData.refreash()
        if check is not None:
            self.label_3.setText(str(check.page_number))
            self.textEdit.setText(check.url)
            self.btn_clicked()

    def btn_clicked_3(self):
        kakao_textPos_x = int(self.plainTextEdit.toPlainText())
        kakao_textPos_y = int(self.plainTextEdit_2.toPlainText())
        kakao_sendPos_x = int(self.plainTextEdit_3.toPlainText())
        kakao_sendPos_y = int(self.plainTextEdit_4.toPlainText())
        if kakao_textPos_x or kakao_textPos_y or kakao_sendPos_x or kakao_sendPos_y is not None:
            print(self.textBrowser.toPlainText())
            clipboard.copy(self.textBrowser.toPlainText())
            pyautogui.moveTo(kakao_textPos_x, kakao_textPos_y)
            pyautogui.click()
            QtTest.QTest.qWait(500)
            pyautogui.hotkey('command', 'v')
            QtTest.QTest.qWait(500)

            pyautogui.moveTo(kakao_sendPos_x, kakao_sendPos_y)
            pyautogui.click()

    def checkPos(self):
        self.label_5.setText(str(pyautogui.position().x))
        self.label_7.setText(str(pyautogui.position().y))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MainWindow()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())