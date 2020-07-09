import time
from datetime import datetime

import cv2
import mss
import mss.tools
import numpy as np
from pyautogui import click, keyDown, keyUp, moveTo, press


class Bot:
    def __init__(self):
        self.mss = mss.mss()
        self.templates = {
            'dino': r'imgs\dino\dino.png',
            'restart': r'imgs\dino\restart.png',
            'score_label': r'imgs\dino\score_label.png'}
        self.threshhold = 0.90
        self.jump_hold_time = 0.093
        self.dino_pos = self._find_dino()
        self.detection_area = {
            'height': 2,
            'width': 40,
            'left': int(self.dino_pos[0] + 55),
            'top': int(self.dino_pos[1])}
        self.game_over_area = {
            'height': 60,
            'width': 60,
            'left': int(self.dino_pos[0] + 245),
            'top': int(self.dino_pos[1] - 55)}
        self.max_detection_area = self.detection_area['left'] + 520

    def __repr__(self):
        return f'<Position Dino: {self.dino_pos}, Detection Area: {self.detection_area}, Threshhold: {self.threshhold}>'

    def _search_template(self, screen, template):
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        return np.where(res >= self.threshhold)

    def _grab_region(self, monitor, grayscale=False, numpy=True):
        img = self.mss.grab(monitor)
        if numpy:
            img = np.array(img, dtype=np.uint8)
        if grayscale:
            return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        return img

    def _expand_detection_area(self):
        if (self.detection_area['left'] < self.max_detection_area):
            self.detection_area['left'] += 3
            self.jump_hold_time -= 0.07
            self.jump_hold_time = 0.093

    def _look_ahead(self):
        img = self._grab_region(self.detection_area, grayscale=True)
        return img.mean()

    def _find_dino(self):
        screen = self._grab_region(self.mss.monitors[1], grayscale=True)
        template = cv2.imread(self.templates['dino'], 0)
        loc = self._search_template(screen, template)
        if not (loc[0] and loc[1]):
            raise RuntimeError('Could not find dino!')
        w, h = template.shape[::-1]
        x, y = next(zip(*loc[:: -1]))
        return x + w/2, y + h/2

    def _game_over(self):
        screen = self._grab_region(self.game_over_area, grayscale=True)
        template = cv2.imread(self.templates['restart'], 0)
        loc = self._search_template(screen, template)
        if loc[0].size and loc[0].size:
            return True
        return False

    def _jump(self):
        keyUp('down')
        keyDown('space')
        time.sleep(self.jump_hold_time)
        keyUp('space')
        press('down', presses=2)
        keyDown('down')

    def play(self):
        try:
            click(*self.dino_pos)
            moveTo(100, 100)
            while not self._game_over():
                if int(self._look_ahead()) < 246:
                    print('[*] object detected')
                    self._jump()
                    self._expand_detection_area()
        except KeyboardInterrupt:
            pass

    def save_score(self):
        screen = self._grab_region(self.mss.monitors[1], grayscale=True)
        template = cv2.imread(self.templates['score_label'], 0)
        loc = self._search_template(screen, template)
        print(loc[0], loc[1])
        if loc[0].size and loc[0].size:
            score_area = {
                'height': 60,
                'width': 200,
                'left': int(loc[1] - 20),
                'top': int(loc[0] - 20)}
            screen = self._grab_region(score_area, numpy=False)
            output = f'game-scores/score-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.png'
            mss.tools.to_png(screen.rgb, screen.size, output=output)


while True:
    bot = Bot()
    print("[**] Bot started")
    bot.play()
    print("[**] Game is over, saving score and restarting")
    bot.save_score()
    time.sleep(2)
    press('space', presses=2, interval=1)
    time.sleep(1)
