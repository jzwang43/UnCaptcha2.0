#!/usr/bin/env python

import pyautogui
import time
import random
import subprocess
import os

try:
    while True:
        pyautogui.dragTo(85, 60, random.randint(5,10)*0.1)
        pyautogui.click(85, 60)
        pyautogui.dragTo(39, 229, 0.8)
        pyautogui.click(39, 229)
        pyautogui.dragTo(140, 638, 0.8)
        pyautogui.click(140, 638)
        pyautogui.dragTo(199, 280, 0.8)
        pyautogui.rightClick(199, 280)
        pyautogui.click(274, 357)
        time.sleep(1)
        pyautogui.hotkey('enter')
        time.sleep(1.5)
        python3_command = "python rec.py"  # launch your python2 script using bash
        process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
        output = process.stdout.readline().decode('utf-8');
        print(output)
        pyautogui.dragTo(167, 231, 1.2)
        pyautogui.click(167, 231)
        pyautogui.typewrite(output);
        pyautogui.hotkey('enter')
        os.remove("audio.mp3")
except KeyboardInterrupt:
    pass
