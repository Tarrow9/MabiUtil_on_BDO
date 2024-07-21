import os
from pynput.keyboard import Listener
from pynput import mouse

from mabisound_source.mabisound import SoundOperator

path = os.path.dirname(os.path.abspath(__file__)) + "\\mabisound_source\\wavfinal"
sound_operator = SoundOperator(path)
with Listener(sound_operator.on_press) as listen:
    with mouse.Listener(on_click = sound_operator.on_click) as listener:
        listener.join()
        listen.join()