import pyautogui as pgui
import time
import os

URL = "https://patrickhlauke.github.io/recaptcha/"
FIREFOX_LOC = 356, 581
CAPTCHA_BOX_LOC = 40, 273
AUDIO_BOX_LOC = 138, 535
AUDIO_DL_LOC = 202, 323

### FIREFOX shortcuts
def refresh_browser():
	pgui.press('f5')

def select_AddressBar():
	pgui.keyDown('Ctrl')
	pgui.press('l')
	pgui.keyUp('Ctrl')	

def open_firefox():
	pgui.dragTo(FIREFOX_LOC)
	pgui.click()

def maximize_window():
	pgui.keyDown('Alt')
	pgui.press('f10')
	pgui.keyUp('Alt')

def goto_URL(url):
	select_AddressBar()
	pgui.typewrite(url)
	pgui.press('enter')
	time.sleep(2)

open_firefox()
time.sleep(2)
goto_URL(URL)

# for i in range(10):
pgui.dragTo(CAPTCHA_BOX_LOC)
pgui.click()
time.sleep(3)
pgui.dragTo(AUDIO_BOX_LOC)
pgui.click()
# tab twice to get the download
pgui.dragTo(AUDIO_DL_LOC)
pgui.rightClick()

#	refresh_browser()
