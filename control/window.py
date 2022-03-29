import win32gui as win
from PIL import ImageGrab
import cv2


def detect(frame):
    bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bw = np.float32(bw)
    
    corners = cv2.cornerHarris(bw, blockSize=4, ksize=3, k=0.04)
    corners = cv2.dilate(corners, None)
    
    max_confidence = corners.max()
    threshold = max_confidence * 0.01
    
    frame[corners > threshold] = [255, 0, 255]
    return frame

phandle = win.FindWindow(None, "Untitled - Notepad")
win.SetForegroundWindow(phandle)

sshot = ImageGrab.grab()
# sshot.show()

import numpy as np

frame = detect(np.array(sshot))
cv2.imshow("Frame", frame)
cv2.waitKey(30000)
