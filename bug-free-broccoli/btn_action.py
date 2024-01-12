from PyQt5 import QtTest, QtWidgets
import pyautogui
import clipboard
import platform
import os
from packages import uData
from main import MainWindow

WAIT_TIME = 20
pyautogui.FAILSAFE = False


def loadPost(main_window: MainWindow):
    url = main_window.lineEdit_URL.text()

    # options
    text = main_window.checkBox_text.isChecked()
    title = main_window.checkBox_title.isChecked()
    dept = main_window.checkBox_dept.isChecked()
    writer = main_window.checkBox_writer.isChecked()
    date = main_window.checkBox_date.isChecked()
    views = main_window.checkBox_views.isChecked()

    global main_post  # TODO: global 키워드를 이용해서 main_post를 강제로 전역변수화시킴. 딱봐도 메모리 문제 있을 것 같음. 근데 지금 당장 어떻게 해결해야할지 모르겠음.
    main_post = uData.init(url, text=text, title=title, dept=dept, writer=writer, date=date, views=views)
    main_post.page_number = int(
        main_window.label_currPostNum.text())  # TODO: 외세에 의해서 POST NUM을 결정하는 방식. 굉장히 안좋아보인다. 그러나 지금당장 어떻게 구현할지 구조가 떠오르지 않아 일단 패스
    main_window.textBrowser_postView.setText(main_post.contents)
    main_post.saveImage()


def checkBoard(main_window: MainWindow):
    current_number = int(main_window.label_currPostNum.text())
    check: uData.update.Refresh = uData.refresh(current_number)
    if check is not None:
        main_window.label_currPostNum.setText(str(check.page_number))
        main_window.lineEdit_URL.setText(check.url)
        loadPost(main_window)


def sendTextToKakao(main_window: MainWindow):
    """
    GUI상에 저장되어있는 게시글 텍스트를 복사해 카카오톡으로 발송합니다.
    :param main_window:
    """
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


def checkPos(main_window: MainWindow):
    main_window.label_mouseXpos.setText(str(pyautogui.position().x))
    main_window.label_mouseYpos.setText(str(pyautogui.position().y))


def resetBoardCheckTimer(main_window: MainWindow):
    main_window.timer.setInterval(main_window.spinBox_updateCycle.value() * 1000)
    main_window.timer.stop()
    main_window.timer.start()


def sendNotification(main_window: MainWindow):
    previousPageNumber = int(main_window.label_currPostNum.text())
    checkBoard(main_window)  # checkBoard가 GUI상의 게시글 번호를 업데이트 해줌.

    if main_post.page_number != previousPageNumber:  # 이전 게시글 넘버와 새롭게 체크한 게시글 넘버가 다르다면, 즉 업데이트된 글이 있다면
        if main_post.hasImage == True:
            sendImageToKakao(main_window)
        sendTextToKakao(main_window)
        resetBoardCheckTimer(main_window)


# TODO: pauseTimer 구현
def pauseTimer(main_window: MainWindow):
    pass


def openImagePath(main_window: MainWindow):
    path = os.path.abspath('images')
    command = f'explorer {path}' if platform.system() == 'Windows' else f'open {path}'
    os.system(command)


def sendImageToKakao(main_window: MainWindow):
    # 폴더 내용 이미지 복사해서 붙여넣기 하는 부분 구현
    explorer_position = (main_window.spinBox_explorerXpos.value(), main_window.spinBox_explorerYpos.value())
    kakao_position = (main_window.spinBox_kakaoXpos.value(), main_window.spinBox_kakaoYpos.value())

    # 컨트롤 키 배정
    ctrl = 'ctrl' if platform.system() == 'Windows' else 'command'

    if platform.system() == 'Windows':  # windows
        # 1. 파일탐색기로 가서 클릭
        pyautogui.click(explorer_position)

        # 2. Ctrl + A를 눌러 파일 전체 선택 후 마우스 30만큼 오른쪽으로 이동
        pyautogui.hotkey(ctrl, 'a')
        pyautogui.moveTo(explorer_position[0] + 30, explorer_position[1], duration=1)
        QtTest.QTest.qWait(100)

        # 3. 카톡창으로 드래그
        pyautogui.dragTo(kakao_position, duration=2, button='left')
        QtTest.QTest.qWait(100)

        # 4. 카톡창 한번 클릭하고 엔터 눌러서 보내기.
        pyautogui.click(kakao_position)
        QtTest.QTest.qWait(100)
        pyautogui.press('Enter')
        for i in range(WAIT_TIME):  # 업로드 될 시간 기다리기
            print(f"wait for {i}")
            QtTest.QTest.qWait(1000)

    else:  # mac os
        # 1. 파일탐색기 가서 한번 클릭.
        pyautogui.click(explorer_position)
        QtTest.QTest.qWait(100)

        # 2. Ctrl + A 누르고 Ctrl + C로 전체 복사 하기
        pyautogui.hotkey(ctrl, 'a')
        QtTest.QTest.qWait(100)
        pyautogui.hotkey(ctrl, 'c')

        # 3. 카카오톡 채팅창 가서 한번 클릭
        pyautogui.click(kakao_position)
        QtTest.QTest.qWait(1000)

        # 4. 붙여넣기 하고 엔터 두 번 눌러서 최종 발송하기
        pyautogui.hotkey(ctrl, 'v')
        pyautogui.press('Enter')
        QtTest.QTest.qWait(100)
        pyautogui.press('Enter')
        for i in range(WAIT_TIME):  # 업로드 될 시간 기다리기
            print(f"wait for {i}")
            QtTest.QTest.qWait(2000)

    # 5. 다시 파일탐색기 가서 이미지 폴더 내용 싹 비우기
    file_list = os.listdir('images')
    for file_name in file_list:
        file_path = os.path.join('images', file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
