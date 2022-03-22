import cv2
from rotation_invariant_match import get_matched_coordinates

needle_image = "game/player.png"
map_image = "vision/map.png"

needle = cv2.imread(needle_image, cv2.IMREAD_GRAYSCALE)
map = cv2.imread(map_image, cv2.IMREAD_GRAYSCALE)

needle = cv2.equalizeHist(needle)
map = cv2.equalizeHist(map)

distances = get_matched_coordinates(needle, map)
print(distances)

# pipenv install opencv-contrib-python
