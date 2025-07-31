from mss import mss
import numpy as np
import cv2
from core.window_utils import get_bbs_window, is_bbs_focused, force_focus_bbs_window, is_fullscreen
from utils.logger import debug
from core.window_utils import is_game_window_valid
from core.esc_listener import start_esc_listener
from utils.logger import warning
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from gui.banner import FloatingBanner

def get_bbs_screenshot():
    win = get_bbs_window()

    if is_fullscreen(win):
        debug("[i] BLEACH is in fullscreen mode — skipping focus and capturing directly.")
    else:
        if not is_bbs_focused():
            debug("Focusing BLEACH window...")
            win = force_focus_bbs_window()

    # Always attempt to capture
    left, top, width, height = win.left, win.top, win.width, win.height
    if width == 0 or height == 0:
        debug("[!] Window appears to be minimized or hidden — skipping capture.")
        return None

    with mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    
def prepare_game_execution(on_escape_callback=None):
    if not is_game_window_valid():
        warning("Game window is invalid. Cannot start.")
        return None

    banner = FloatingBanner()
    banner.show()

    # Force the UI to update before continuing
    QApplication.processEvents()

    return banner