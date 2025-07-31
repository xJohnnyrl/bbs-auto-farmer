from core.state import state, GameState
import time
from core.actions import find_and_click_image, check_image_present
from utils.logger import debug, error
from utils.settings import settings
from core.stop_controller import stop_controller
from core.capture import get_bbs_screenshot
from core.logic.end_menu import handle_end_menu

def handle_gameplay_single_player():
        while not stop_controller.should_stop():
            screenshot = get_bbs_screenshot()
            # Check for auto
            auto_enabled = find_and_click_image("assets/icons/auto_off.png", screenshot=screenshot)
            if auto_enabled:
                debug("[Auto] Auto was off — activating.")
            else:
                debug("[Auto] Already on.")
                
            # Check for revive candles
            revive_candles = check_image_present("assets/icons/continue_check.png", screenshot=screenshot)
            if revive_candles and settings["use_revive_candles"]:
                debug("[Revive Candles] All characters died activating revive candles.")
                find_and_click_image("assets/icons/ok.png", screenshot=screenshot)
                time.sleep(2)
                find_and_click_image("assets/icons/ok.png", screenshot=screenshot)
            elif revive_candles and not settings["use_revive_candles"]:
                debug("[Revive Candles] All characters died but revive candles are disabled.")
                find_and_click_image("assets/icons/quit.png", screenshot=screenshot)
                debug("[Game] Quest finished.")
                break
            else:
                debug("[Revive Candles] All characters are alive.")
            
            find_and_click_image("assets/icons/skip.png", screenshot=screenshot)
            
            # Check for end screen
            if any(
                check_image_present(f"assets/icons/{t}.png", screenshot=screenshot)
                for t in ["tap_screen", "cancel", "tap_here_to_continue", "close"]
            ):
                debug("[Game] Quest finished.")
                break
            
            time.sleep(1)