import cv2
import numpy as np

def detect(frame):
    bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bw = np.float32(bw)
    
    corners = cv2.cornerHarris(bw, blockSize=4, ksize=3, k=0.002)
    corners = cv2.dilate(corners, None)
    
    max_confidence = corners.max()
    threshold = max_confidence * 0.0005
    
    frame[corners > threshold] = [255, 0, 255]
    return frame