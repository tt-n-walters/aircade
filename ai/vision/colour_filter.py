import cv2
import numpy as np

import time

from ..control.window import take_screenshot

PLAYER_COLOUR = np.array([245, 187, 54])


image = cv2.imread("ai/vision/map.png", cv2.IMREAD_UNCHANGED)

print(image.shape)
map = cv2.inRange(image, PLAYER_COLOUR, PLAYER_COLOUR)
coords = np.array(np.where(map)).T

# Find min/max values of x and y
# Calculate a midpoint
min_x = coords[:, 1].min()
max_x = coords[:, 1].max()
min_y = coords[:, 0].min()
max_y = coords[:, 0].max()

corners = np.array([[min_y, min_x],
                    [max_y, max_x]])
center = corners.mean(axis=0).round().astype(int)

# Calculate mean pixel coordinate
mean = coords.mean(axis=0).round().astype(int)

print("center", center)
print("mean", mean)
print(mean.dtype)


cv2.line(image, mean[::-1], center[::-1], (0, 255, 255), 3)
cv2.imshow("Image", image)
cv2.waitKey(0)