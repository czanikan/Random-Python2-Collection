import win32api, win32con, time, os

clear = lambda: os.system('cls')

isRec = True
isPlayed = False
cursorPosMemory = []
leftClickMemory = []

def main():
    print "Hold [CTRL] + [SHIFT] + [R] to record action."

    while not (win32api.GetAsyncKeyState(ord('R')) and win32api.GetAsyncKeyState(win32con.VK_CONTROL) and win32api.GetAsyncKeyState(win32con.VK_SHIFT)):
         pass
    
    while (win32api.GetAsyncKeyState(ord('R')) and win32api.GetAsyncKeyState(win32con.VK_CONTROL) and win32api.GetAsyncKeyState(win32con.VK_SHIFT)):
        recordActions()
        clear()
        print "Recording..."

    clear()
    # print cursorPosMemory

    print "Press [SPACE] to replay action."

    while True:
        if win32api.GetAsyncKeyState(win32con.VK_SPACE):
            replayActions()     

    term = input("Press [ENTER] to terminate.")

def recordActions():
    # Record Cursor Position
    pos=win32api.GetCursorPos()
    cursorPosMemory.append(pos)
    # Record left click states
    leftClickMemory.append(win32api.GetAsyncKeyState(1))
    time.sleep(0.01)

def replayActions():
    for i in range(len(cursorPosMemory)):
        win32api.SetCursorPos(cursorPosMemory[i])
        if leftClickMemory[i] < 0:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        time.sleep(0.125)

    # Reset left click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)


if __name__ == "__main__":
	main()
