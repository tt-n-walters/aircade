import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import threading
import time
import numpy as np

from ..game.main import run_game


def check_game_open(window_title):
    """
    window_title: str  -> Title of the window to search for

    Returns:
    bool   -> If window is open or not
    """
    titles = []
    def handle_function(handle, extra):
        title = win32gui.GetWindowText(handle)
        if title:
            titles.append(title)

    win32gui.EnumWindows(handle_function, None)
    return window_title in titles


def take_screenshot(handle):
    """
    handle: int   -> Handle of a currently open window

    Returns:
    np.array   -> Cropped screenshot of desired window
    """
    bbox = win32gui.GetClientRect(handle)
    left, top, right, bottom = bbox
    width, height = right - left, bottom - top

    dc_handle = win32gui.GetDC(handle)
    device_context = win32ui.CreateDCFromHandle(dc_handle)
    compatile_dc = device_context.CreateCompatibleDC()

    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(device_context, width, height)

    compatile_dc.SelectObject(bitmap)
    windll.user32.PrintWindow(handle, compatile_dc.GetSafeHdc(), 1)

    image_data = bitmap.GetBitmapBits(True)
    image = Image.frombuffer("RGB", (width, height), image_data, "raw", "BGRX", 0, 1)

    image.save("ai/vision/map.png")
    return np.array(image)


def start_game():
    game_thread = threading.Thread(target=run_game)
    game_thread.start()
    return game_thread


def search_game_window(title):
    start_time = time.time()
    window_found = False
    while not window_found and time.time() < (start_time + 5):
        window_found = check_game_open(title)
        time.sleep(0.5)

    if window_found:
        handle = win32gui.FindWindow(None, title)
        return handle


if __name__ == "__main__":
    # start_game()
    # if handle := search_game_window():
    #     take_screenshot(handle)

    handle = search_game_window("AIrcade")
    if handle:
        take_screenshot(handle)
