import sys
import pyautogui

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt 
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("test.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.fore = pyautogui.getActiveWindow()

        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()
        screenWidth = screenRect.width()
        self.setGeometry(screenWidth - 550, 200, 200, 50)

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