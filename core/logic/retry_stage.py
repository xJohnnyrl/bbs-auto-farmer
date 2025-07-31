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

def retry_stage():
    stop_controller.reset() 
    
    banner = prepare_game_execution(lambda: stop_controller.stop())
    if not banner:
        return
    
    start_esc_listener(lambda: (
        stop_controller.stop(),
        banner.close()
    ))
    
    if settings["auto_set_boost_to_max"]:
        screenshot = get_bbs_screenshot()
        debug("[Boost] Auto setting boost to max.")
        if (check_image_present("assets/icons/max_boost.png", screenshot=screenshot)):
            debug("[Boost] Boost is already max.")
        else:
            find_and_click_image("assets/icons/boost_1.png", screenshot=screenshot)
            find_and_click_image("assets/icons/boost_2.png", screenshot=screenshot)
            screenshot = get_bbs_screenshot()
            for i in range(9):
                find_and_click_image("assets/icons/boost_increase.png", double_click=True, screenshot=screenshot)
        
    orbs_used = 0
    tickets_used = 0
    quest_completed = False
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

            if check_image_present("assets/icons/purchase.png", screenshot=screenshot):
                debug("[Stage] Purchase screen detected.")
                if (orbs_used >= settings["max_orbs"] or (orbs_used + 9) >= settings["max_orbs"]) and settings["max_orbs"] != 0:
                    debug("[Tickets] Max orbs reached.")
                    break
                orbs_used = handle_tickets(orbs_used, settings["max_orbs"])
                continue
            else:
                debug("[Stage] Quest started using tickets.")
            
        elif check_image_present("assets/icons/pause.png", screenshot=screenshot):
            debug("[Stage] Detected in-game. Running gameplay handler.")
            handle_gameplay()
            quest_completed = handle_end_menu() 
            
        if quest_completed:
            tickets_used += 10 if settings["auto_set_boost_to_max"] else 1
        
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