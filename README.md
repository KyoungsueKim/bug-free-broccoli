# bug-free-broccoli
아주대학교 공지사항 게시물을 자동으로 크롤링 해 카카오톡 채팅방으로 전달해주는 공지 봇 프로그램입니다.

<img src="https://user-images.githubusercontent.com/61102713/147847081-877431f2-a4b3-4f3e-857f-dace814e1082.gif" alt="ezgif com-gif-maker-2" style="max-width: 100%;">

위 그림과 같이 발송을 원하는 채팅방 창과, bug-free-broccoli/images 폴더가 열린 탐색기 창, 그리고 main.py가 실행된 창이 한 화면에 같이 있어야합니다. 

현재 오픈베타가 진행중입니다. 체험해보고 싶으시다면 https://bit.ly/3qFhwvR 여기에 접속해 아주대학교 실시간 공지사항 채팅방에 참여해보세요. 채팅방 비번은 배경화면에 있습니다. 

## Achievement
<img width="447" alt="image" src="https://user-images.githubusercontent.com/61102713/147847305-7441f9b9-239f-43a5-8910-f7d6eb3bca69.png">
* 2022년 1월 1일 기준으로 795명의 학생들이 아주대학교 실시간 공지사항을 사용해주시고 계십니다. 

## Prerequisite
* `pyqt5` ~= 5.15.4
* `bs4` ~= 0.0.1
* `beautifulsoup4` ~= 4.9.3
* `requests` ~= 2.26.0
* `urllib3` ~= 1.26.6
* `pyshorteners` ~= 1.0.1
* `pyautogui` ~= 0.9.53
* `clipboard` ~= 0.0.4

## Installation
```Shell
git clone https://github.com/KyoungsueKim/bug-free-broccoli
cd bug-free-broccoli
pip install -r requirements.txt
```

## Run
```Shell
python3 bug-free-broccoli/main.py
```
