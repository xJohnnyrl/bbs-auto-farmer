from core.actions import find_and_click_image, check_image_present
import time
from utils.logger import debug
from core.stop_controller import stop_controller
from core.capture import get_bbs_screenshot

def handle_end_menu():
    last_icon = None
    times_tried = 0

    while not stop_controller.should_stop():
        screenshot = get_bbs_screenshot()
        icon_clicked = False

        for icon in ["tap_screen", "cancel", "close", "retry", "tap_here_to_continue"]:
            if find_and_click_image(f"assets/icons/{icon}.png", double_click=(icon == "tap_screen" or icon == "tap_here_to_continue"), screenshot=screenshot):
                debug(f"[Game] Clicked '{icon}'.")
                if icon == "retry":
                    return True
                time.sleep(2)
                last_icon = icon
                times_tried = 0
                icon_clicked = True
                break

        if not icon_clicked:
            debug("[Game] No icon found.")
            time.sleep(1)
            times_tried += 1

            if times_tried > 5:
                debug("[Game] No icon found. Exiting.")
                return False