import cv2
from PIL import Image, ImageFilter
import numpy as np

from . import corner_detection


def make_image_weird(frame):
    global offset
    frame[:, :, 0] =  - frame[:, :, 0] + offset + frame[:, ::-1, 0]
    frame[:, :, 1] =  - frame[:, :, 1] + offset*2
    frame[:, :, 2] =  - frame[:, :, 2] + frame[::-1, :, 2]
    offset += 1
    img = Image.fromarray(frame).filter(ImageFilter.CONTOUR)
    frame = np.array(img)


video = cv2.VideoCapture(0)
# video.set(3, 1280)
# video.set(4, 720)

offset = 0

if video.isOpened():
    while True:
        ret_v, frame = video.read()
        
        frame = corner_detection.detect(frame)
        make_image_weird(frame)
        
        cv2.imshow("Window", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
