import win32api, win32con, time, os, atexit

exc=False

clear = lambda: os.system('cls')

def main():
	min = 0
	hour = 0
	day = 0

	while True:
		
		try:
			consoleUpdate(day, hour, min)
			#result = win32api.MessageBox(0,"Something went wrong :c", "Error")
			pos=win32api.GetCursorPos()
			time.sleep(60)
			curPos=win32api.GetCursorPos()
				
			min += 1
		
			if min % 60 == 0:
				min = 0
				hour += 1
				if hour % 24 == 0:
					hour = 0
					day += 1
		
			if pos == curPos:
				win32api.keybd_event(0xAD, 0,0,0)
				time.sleep(.05)
				win32api.keybd_event(0xAD,0 ,win32con.KEYEVENTF_KEYUP ,0)
				time.sleep(.05)
				win32api.keybd_event(0xAD, 0,0,0)
				time.sleep(.05)
				win32api.keybd_event(0xAD,0 ,win32con.KEYEVENTF_KEYUP ,0)
				exc=False
		except:
			if not exc:
				print "Something went wrong..."
				exc=True

def consoleUpdate(day, hour, min):
	os.system('cls')
	print("Screensaver Saver")
	print("v.2.4.3")
	print("-" * 50)
	print("Time passed since: " + str(day) + " : " + str(hour) + " : " + str(min))

if __name__ == "__main__":
	main()
