from PyQt5 import QtTest, QtWidgets
import pyautogui
import clipboard
import platform
from packages import uData
from main import MainWindow

def btn_loadPost(main_window: MainWindow):
    url = main_window.lineEdit_URL.text()

    # option
    text = main_window.checkBox_text.isChecked()
    title = main_window.checkBox_title.isChecked()
    dept = main_window.checkBox_dept.isChecked()
    writer = main_window.checkBox_writer.isChecked()
    date = main_window.checkBox_date.isChecked()
    views = main_window.checkBox_views.isChecked()

    post01 = uData.init(url, text=text, title=title, dept=dept, writer=writer, date=date, views=views)
    main_window.textBrowser_postView.setText(post01.contents)
    if post01.isImageExist is True:
        None
    else:
        None

def btn_checkBoard(main_window: MainWindow):
    check: uData.update.Refresh = uData.refresh()
    if check is not None:
        main_window.label_currPostNum.setText(str(check.page_number))
        main_window.lineEdit_URL.setText(check.url)
        btn_loadPost(main_window)

def btn_sendKakao(main_window: MainWindow):
    kakao_textPos_x = main_window.spinBox_kakaoXpos.value()
    kakao_textPos_y = main_window.spinBox_kakaoYpos.value()
    if kakao_textPos_x and kakao_textPos_y is not None:
        clipboard.copy(main_window.textBrowser_postView.toPlainText())
        pyautogui.moveTo(kakao_textPos_x, kakao_textPos_y)
        pyautogui.click()
        QtTest.QTest.qWait(100)

        ctrl = 'ctrl' if platform.system() == 'Windows' else 'command'
        pyautogui.hotkey(ctrl, 'v')
        QtTest.QTest.qWait(1000)
        pyautogui.press('Enter')

    resetBoardCheckTimer(main_window)

def checkPos(main_window: MainWindow):
    main_window.label_mouseXpos.setText(str(pyautogui.position().x))
    main_window.label_mouseYpos.setText(str(pyautogui.position().y))

def resetBoardCheckTimer(main_window: MainWindow):
    main_window.timer.setInterval(main_window.spinBox_updateCycle.value() * 1000)
    main_window.timer.stop()
    main_window.timer.start()

def checkBoardAndSendKakao(main_window: MainWindow):
    currentPageNumber = int(main_window.label_currPostNum.text())
    btn_checkBoard(main_window)
    if uData.Refresh.page_number != currentPageNumber:
        btn_sendKakao(main_window)

def pauseTimer(main_window: MainWindow):
    None

if __name__ == "__main__":
    pass