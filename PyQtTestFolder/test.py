import sys
import pyautogui
import json

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt , QEvent
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("test.ui")[0]

# 설정값 로드
pyqt_config = {}
with open('./config.json') as config_fp:
    pyqt_config = json.load(config_fp)

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        # self.setAttribute(Qt.WA_NoChildEventsForParent, True)
        self.setWindowFlags(Qt.Window|Qt.X11BypassWindowManagerHint|Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        self.fore = pyautogui.getActiveWindow()
        self.conf_pos = pyqt_config['position']

        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()
        screenWidth = screenRect.width()
        self.setGeometry(
            screenWidth + self.conf_pos.get('ax', -320), 
            self.conf_pos.get('ay', 350), 
            self.conf_pos.get('width', 300), 
            self.conf_pos.get('height', 50)
        )
        self.setFocusPolicy(Qt.StrongFocus)

        self.click_through_flag = False

    def showEvent(self, event):
        super().showEvent(event)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
    



    
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isActiveWindow():
                # 윈도우가 활성화된 경우, 마우스 이벤트를 받도록 설정
                self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            else:
                # 윈도우가 비활성화된 경우, 마우스 이벤트를 무시하도록 설정
                self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            print(f"ChangeEvent - TransparentForMouseEvents: {self.testAttribute(Qt.WA_TransparentForMouseEvents)}")
        super().changeEvent(event)

    def focusInEvent(self, event):
        print('focusInEvent')
        # 포커스를 받을 때 마우스 이벤트를 받도록 설정
        if self.isActiveWindow():
            self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        print(f"FocusInEvent - TransparentForMouseEvents: {self.testAttribute(Qt.WA_TransparentForMouseEvents)}")
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        print('focusOutEvent')
        # 포커스를 잃었을 때 마우스 이벤트를 무시하도록 설정
        if not self.isActiveWindow():
            self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        print(f"FocusOutEvent - TransparentForMouseEvents: {self.testAttribute(Qt.WA_TransparentForMouseEvents)}")
        super().focusOutEvent(event)

    def contextMenuEvent(self, event: QContextMenuEvent):
        context_menu = QMenu(self)
        click_through_flag = QAction("마우스 비활성화(윈도우 포커스시 해제)", self)
        add_alarm = QAction("알람 추가", self)
        del_alarm = QAction("알람 삭제", self)
        context_menu.addAction(click_through_flag)
        context_menu.addAction(add_alarm)
        context_menu.addAction(del_alarm)
        context_menu.exec_(event.globalPos())


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    # font
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./sources/MabiOldTxt_v0.3_HeightUp.ttf')
    app.setFont(QFont('MabiOldTxt', 9))

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()