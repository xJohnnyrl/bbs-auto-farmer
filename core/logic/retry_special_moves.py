import time
from core.state import state, GameState
from core.actions import find_and_click_image, check_image_present
from core.logic.gameplay import handle_gameplay
from core.logic.end_menu import handle_end_menu
from utils.logger import debug, error
from core.capture import prepare_game_execution
from core.stop_controller import stop_controller
from core.esc_listener import start_esc_listener
from utils.settings import settings
from core.logic.collect_tickets import handle_tickets
from core.capture import get_bbs_screenshot

def special_moves_stage():
    stop_controller.reset() 
    
    banner = prepare_game_execution(lambda: stop_controller.stop())
    if not banner:
        return
    
    start_esc_listener(lambda: (
        stop_controller.stop(),
        banner.close()
    ))
    
    orbs_used = 0
    tickets_used = 0
    quest_completed = False
    not_findable_amount = 0
    while should_continue(tickets_used):
        screenshot = get_bbs_screenshot()
        if check_image_present("assets/icons/menu_check.png", screenshot=screenshot):
            debug("[Stage] In menu.")

            if not find_and_click_image("assets/icons/start_quest.png", screenshot=screenshot):
                error("Failed to click 'Start Quest'")
                time.sleep(2)
                continue

            time.sleep(1)
            screenshot = get_bbs_screenshot()

            find_and_click_image("assets/icons/ok.png", screenshot=screenshot)

            debug("[Stage] Quest started using tickets.")
            
        elif check_image_present("assets/icons/pause.png", screenshot=screenshot):
            debug("[Stage] Detected in-game. Running gameplay handler.")
            handle_gameplay()
            quest_completed = handle_end_menu() 

        else:
            not_findable_amount += 1
            if not_findable_amount > 10:
                error("[Stage] Not findable amount reached, stopping.")
                break

        if quest_completed:
            tickets_used += 1
        
        quest_completed = False
        debug(f"[Tracker] Tickets used: {tickets_used} | Orbs used: {orbs_used}")
        time.sleep(5)
   
    stop_controller.stop()
    banner.close()
    return orbs_used, tickets_used

def should_continue(tickets_used: int) -> bool:
    if stop_controller.should_stop():
        return False

    max_tickets = settings["max_tickets"]
    boost_amount = 9 if settings["auto_set_boost_to_max"] else 0

    if max_tickets == -1:
        return True

    return (
        tickets_used < max_tickets and
        (tickets_used + boost_amount) < max_tickets
    )