import sys
from time import sleep

from pyautogui import (ImageNotFoundException, center, click,
                       displayMousePosition, locate, moveTo, screenshot)

exp = str(sys.argv[1])

n = {**{str(i): f'imgs/calc/key{i}.png' for i in range(10)},
     '+': 'imgs/calc/sum.png',
     '-': 'imgs/calc/sub.png',
     'x': 'imgs/calc/mul.png',
     '/': 'imgs/calc/div.png',
     '=': 'imgs/calc/eq.png'}

clicks = []
for c in exp:
    try:
        sshot = screenshot(region=(1450, 0, 470, 640))
        l = locate(n[c], sshot, grayscale=True)
    except ImageNotFoundException as e:
        print(e)
    else:
        clicks.append(center(l))

print(clicks)

for p in clicks:
    click(1450 + p.x, p.y)

