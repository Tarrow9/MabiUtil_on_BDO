from utils import Singleton
from paddleocr import PaddleOCR
import mss
import mss.tools
import pygame

pygame.init()

@Singleton
class MabiBGM:
    def __init__(self, path, left, top, width, height):
        self.ocr = PaddleOCR(lang="korean")
        self.location_dict = {
            '벨리아': '~티르코네일브금파일~',
            '하이델': '~던바튼브금파일~',
            '칼페온': path + "\\inventory_open.wav",
        }
        self.minimap_pos = {
            "left": left,
            "top": top,
            "width": width,
            "height": height
        }
        self.mixer = pygame.mixer
        self.now_bgm = None
    
    def set_minimap_pos(self, left, top, width, height):
        self.minimap_pos = {
            "left": left,
            "top": top,
            "width": width,
            "height": height
        }
    
    def capture_location(self) -> bytes:
        with mss.mss() as screen:
            sct_img = screen.grab(self.minimap_pos)
            raw_bytes = mss.tools.to_png(sct_img.rgb, sct_img.size)
        return raw_bytes

    def run_ocr(self, img_bytes: bytes) -> str:
        sentence_list = []
        paddle_result = self.ocr.ocr(img_bytes, cls=False)
        for sentence in paddle_result[0]:
            sentence_list.append(sentence[1][0])
        result = ''.join(sentence_list)
        return result
    
    def play_bgm(self, current_loc):
        if current_loc in self.location_dict:
            if self.mixer.get_busy():
                self.mixer.stop()
                self.now_bgm
                self.now_bgm = self.location_dict[current_loc]
                self.now_bgm.play()
        else:
            pass
    
    def turn_on(self):
        pass