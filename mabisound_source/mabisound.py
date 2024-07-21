from pynput.keyboard import Key, Listener
from pynput import mouse
from pynput.mouse import Button
import pygame
import random

import pyautogui

pygame.init()

class SoundArchive:
    def __init__(self, path):
        self.mapopen = pygame.mixer.Sound(path + "\\inventory_open.wav")
        self.mapclose = pygame.mixer.Sound(path + "\\inventory_close.wav")
        self.windowopen = pygame.mixer.Sound(path + "\\gen_window_open.wav")
        self.windowclose = pygame.mixer.Sound(path + "\\gen_window_closed.wav")
        self.clicksound1 = pygame.mixer.Sound(path + "\\gen_button_confirm.wav")
        self.clicksound2 = pygame.mixer.Sound(path + "\\gen_button_down.wav")
        self.emotion_fail= pygame.mixer.Sound(path + "\\emotion_fail.wav")
        self.emotion_success = pygame.mixer.Sound(path + "\\emotion_success.wav")
        self.emotion_success_giant = pygame.mixer.Sound(path + "\\emotion_success_giant.wav")
        self.enchant_success = pygame.mixer.Sound(path + "\\enchant_success.wav")
    
    #TODO: Test
    def volume_control(
            self, 
            sound_instance: pygame.mixer.Sound, 
            volume: float
        ):
        sound_instance.set_volume(volume)

class SoundOperator:
    def __init__(self, path):
        self.mouse_stat = 0 #전체 스탯
        self.RU_gathering_now = 0 #현재 채집을 하고 있는지
        self.last = pygame.time.get_ticks()
        self.cooldown = 2472
        self.sound_archive = SoundArchive(path)
        self.fore = pyautogui.getActiveWindow()

    def _change_mouse_stat(self, mousestat: int):
        if mousestat == 0:
            self.mouse_stat = 1
        else:
            self.mouse_stat = 0
            
    def _change_gathering_stat(self, gatheringstat: int):
        if gatheringstat == 0:
            self.RU_gathering_now = 1
        else:
            self.RU_gathering_now = 0

    def _gathering_get(self):
        now = pygame.time.get_ticks()
        if now - self.last > self.cooldown:
            self.last = now
            self.sound_archive.emotion_success.play()

    def _gathering_inittime(self):
        now = pygame.time.get_ticks()
        self.last = now

    def on_click(self, x, y, button, pressed):
        # 검은사막 켜져있을 때만 키소리 나게함
        if self.fore.title[:4] != "검은사막":
            return

        if pressed:
            if self.mouse_stat == 1 and (button == Button.left or button == Button.right):
                if round(random.random()*10000) < 7500:
                    self.sound_archive.clicksound2.play()
                else:
                    self.sound_archive.clicksound1.play()

    def on_press(self, key):
        # 검은사막 켜져있을 때만 키소리 나게함
        if self.fore.title[:4] != "검은사막":
            return

        windowlist = ['y','i','o','p','g','k','l','b','n']
        movelist = ['a','w','s','d']
        try:
            #기능창 열 시 마우스 생김
            if key.char in windowlist: 
                self._change_mouse_stat(self.mouse_stat)
                self.sound_archive.windowopen.play()

            #움직일 시 마우스커서 그냥 없어짐
            elif key.char in movelist:
                self._gathering_inittime()
                self.mouse_stat = 0

            #마우스 생기게하는 키
            elif key.char == '`':
                self._change_mouse_stat(self.mouse_stat)

            #맵 여는 키
            elif key.char == 'm':
                if self.mouse_stat == 0:
                    self.mouse_stat = 1
                self.sound_archive.mapopen.play()

            #쓰레드를 이용해서 소리들리도록 함 (채집)
            elif key.char == 'r':
                if self.RU_gathering_now == 0:
                    self._change_mouse_stat(self.mouse_stat)
                else:
                    self._gathering_get()

        except AttributeError:
            if key == Key.esc:
                self._change_mouse_stat(self.mouse_stat)
                self.sound_archive.windowclose.play()
            elif key == Key.f2:
                self.mouse_stat = 0
            elif key == Key.menu:
                self._change_gathering_stat(self.RU_gathering_now)
                print("gathering status =", self.RU_gathering_now)
            elif key == Key.f9:
                self.sound_archive.emotion_fail.play()
            elif key == Key.f10:
                self.sound_archive.emotion_success.play()
            elif key == Key.f11:
                self.sound_archive.emotion_success_giant.play()
            elif key == Key.f12:
                self.sound_archive.enchant_success.play()
            elif key == Key.shift:
                self._gathering_inittime()
                self.mouse_stat = 0
