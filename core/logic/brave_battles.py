import time
from core.actions import find_and_click_image, check_image_present
from utils.logger import debug, error
from core.capture import prepare_game_execution
from core.stop_controller import stop_controller
from core.esc_listener import start_esc_listener
from utils.settings import settings
from core.capture import get_bbs_screenshot
from core.logic.handle_gameplay_single_player import handle_gameplay_single_player
from core.logic.end_menu_singleplayer import handle_end_menu_singleplayer

def brave_battles():
    stop_controller.reset() 
    
    banner = prepare_game_execution(lambda: stop_controller.stop())
    if not banner:
        return "Game window not found. Please make sure the game is open and properly positioned."
    
    start_esc_listener(lambda: (
        stop_controller.stop(),
        banner.close()
    ))
    
    battles_completed = 0
    
    while not stop_controller.should_stop():
        screenshot = get_bbs_screenshot()
        
        # Check if we're on the PvP screen
        if check_image_present("assets/icons/brave_battle_check.png", screenshot=screenshot):
            debug("[Brave Battles] On PvP screen - looking for battle button")
            
            # Look for the battle button
            if check_image_present("assets/icons/brave_battles_battle.png", screenshot=screenshot):
                debug("[Brave Battles] Found battle button, clicking on it")
                
                # Click on the battle button
                if find_and_click_image("assets/icons/brave_battles_battle.png", screenshot=screenshot):
                    time.sleep(1)
                    debug("[Brave Battles] Started battle")
                    
                    # Handle the battle
                    battle_completed = handle_brave_battles()
                    if battle_completed:
                        battles_completed += 1
                        debug(f"[Brave Battles] Completed battle {battles_completed}")
                        
                        # Check if we've reached the limit
                        if settings["brave_battles_tickets"] != -1 and battles_completed >= settings["brave_battles_tickets"]:
                            debug(f"[Brave Battles] Reached limit of {settings['brave_battles_tickets']} battles")
                            break
                    else:
                        debug("[Brave Battles] Battle failed or was interrupted")
                        return "Battle failed or was interrupted"
                else:
                    debug("[Brave Battles] Could not click on battle button")
                    return "Could not click on battle button"
            else:
                debug("[Brave Battles] No battle button found")
                return "No battle button found on PvP screen"
                
        else:
            debug("[Brave Battles] Not on PvP screen")
            return "Not on PvP screen. Please navigate to Brave Battles first."
        
        # Check for stop condition before sleep
        if stop_controller.should_stop():
            break
            
        time.sleep(2)
   
    stop_controller.stop()
    banner.close()
    return f"Completed {battles_completed} battles"

def handle_brave_battles():
    """Handle a single Brave Battle."""
    debug("[Brave Battle] Starting battle")
    
    battle_completed = False
    
    while not stop_controller.should_stop():
        screenshot = get_bbs_screenshot()
        
        # Check for start battle button
        if check_image_present("assets/icons/tap_screen_brave_battles.png", screenshot=screenshot):
            if find_and_click_image("assets/icons/tap_screen_brave_battles.png", screenshot=screenshot):
                time.sleep(1)
                battle_completed = True
                break
        
        time.sleep(1)
    
    return battle_completed