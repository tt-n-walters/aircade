import cv2
import numpy as np

import time

from ..control.window import take_screenshot, search_game_window


PLAYER_PRIMARY_COLOUR = np.array([245, 187, 54])
PLAYER_SECONDARY_COLOUR = np.array([85, 60, 74])


def delta_to_angle(delta):
    angle = np.degrees(np.arctan(delta[0] / delta[1]))

    if delta[1] < 0:
        angle += 180
    angle += 90

    return angle


# print(delta_to_angle([1, 1]))
# print(delta_to_angle([1, -1]))
# print(delta_to_angle([-1, -1]))
# print(delta_to_angle([-1, 1]))
# exit()

handle = search_game_window("AIrcade")

while True:
    image = cv2.cvtColor(take_screenshot(handle), cv2.COLOR_RGB2BGR)

    map_primary = cv2.inRange(image, PLAYER_PRIMARY_COLOUR*0.75, PLAYER_PRIMARY_COLOUR*1.25)
    primary_coords = np.array(np.where(map_primary)).T
    
    map_secondary = cv2.inRange(image, PLAYER_SECONDARY_COLOUR, PLAYER_SECONDARY_COLOUR)
    secondary_coords = np.array(np.where(map_secondary)).T

    # Find min/max values of x and y
    # Calculate a midpoint
    min_x = primary_coords[:, 1].min()
    max_x = primary_coords[:, 1].max()
    min_y = primary_coords[:, 0].min()
    max_y = primary_coords[:, 0].max()

    corners = np.array([[min_y, min_x],
                        [max_y, max_x]])

    # Calculate mean pixel coordinate
    primary_mean = primary_coords.mean(axis=0)
    secondary_mean = secondary_coords.mean(axis=0)

    delta = secondary_mean - primary_mean
    angle = delta_to_angle(delta)
    print(delta, angle)
    end = primary_mean + delta * 10

    # print("center", center)
    # print("mean", mean)
    # print(mean.dtype)


    cv2.line(
        image,
        primary_mean[::-1].round().astype(int),
        end[::-1].round().astype(int),
        (0, 255, 255), 3
    )
    cv2.rectangle(
        image,
        [min_x, min_y],
        [max_x, max_y],
        (0, 255, 0), 3
    )
    # cv2.rectangle(image, mean.round().astype(int)[::-1], mean.round().astype(int)[::-1], (0, 0, 255))
    # cv2.rectangle(image, center.round().astype(int)[::-1], center.round().astype(int)[::-1], (0, 0, 255))
    # cv2.rectangle(image, corners_center.round().astype(int)[::-1], corners_center.round().astype(int)[::-1], (255, 0, 255))
    cv2.imshow("Image", image)
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
