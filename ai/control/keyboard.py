from audioop import add
import win32gui
import win32con
import time
from threading import Thread


from .window import search_game_window

def press_key_thread(handle, key, duration, delay=0):
    keycode = ord(key.upper())
    if delay:
        time.sleep(delay)
    win32gui.SendMessage(handle, win32con.WM_KEYDOWN, keycode, 0)
    time.sleep(duration)
    win32gui.SendMessage(handle, win32con.WM_KEYUP, keycode, 1<<30)


def press_key(handle, key, duration, delay=0):
    thread = Thread(target=press_key_thread,
                    args=(handle, key, duration),
                    kwargs={"delay": delay})
    thread.start()
    return thread


if __name__ == "__main__":
    handle = search_game_window("AIrcade")

    press_key(handle, "a", 0.5)
    press_key(handle, "w", 2, delay=0.5)