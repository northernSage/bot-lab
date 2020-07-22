import win32api
import win32con
from time import sleep

while True:
    if win32api.GetAsyncKeyState(0x51):
        print('q was pressed!')
        sleep(0.5)
