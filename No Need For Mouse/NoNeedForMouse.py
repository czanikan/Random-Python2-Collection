import win32api, win32con, time, os
from ctypes import *

clear = lambda: os.system('cls')
movespeed = 5
xMove = 0
yMove = 0

def main():
    ok = windll.user32.BlockInput(True)
    while True:
        
        if (win32api.GetAsyncKeyState(win32con.VK_MULTIPLY)):
            currentPos = win32api.GetCursorPos()
            newPos = currentPos
            xMove = 0
            yMove = 0
            if win32api.GetAsyncKeyState(ord('A')):
                xMove = -movespeed
            if win32api.GetAsyncKeyState(ord('D')):
                xMove = movespeed
            if win32api.GetAsyncKeyState(ord('W')):
                yMove = -movespeed
            if win32api.GetAsyncKeyState(ord('S')):
                yMove = movespeed
            newPos = (currentPos[0] + xMove, currentPos[1] + yMove)
            win32api.SetCursorPos(newPos)
            

            if win32api.GetAsyncKeyState(ord('Q')):
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
            
            if win32api.GetAsyncKeyState(ord('E')):
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

            time.sleep(0.01)

if __name__ == "__main__":
	main()
