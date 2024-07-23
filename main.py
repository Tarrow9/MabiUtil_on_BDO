"""
    추후 이곳은 pyqt 메인 윈도우가 뜨도록 하는 코드가 적힘미다.
"""
import os
import threading
from pynput.keyboard import Listener
from pynput import mouse

from mabisound_source.mabisound import SoundOperator

# 테스트용임미다.
if __name__=='__main__':
    stop_event = threading.Event()

    path = os.path.dirname(os.path.abspath(__file__)) + "\\mabisound_source\\wavfinal"
    sound_operator = SoundOperator(path)

    keyboard_listener = Listener(sound_operator.on_press)
    mouse_listener = mouse.Listener(on_click = sound_operator.on_click)

    keyboard_listener.start()
    mouse_listener.start()

    stop_event.set()

# 이곳엔 PyQt5 코드가 들어올 것임미다.
# 메인을 실행하면 사운드유틸이 스레드로 실행되고
# PyQt창이 띄워짐미다.