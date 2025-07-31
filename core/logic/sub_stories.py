import time
from core.actions import find_and_click_image, check_image_present
from utils.logger import debug, error
from core.capture import prepare_game_execution
from core.stop_controller import stop_controller
from core.esc_listener import start_esc_listener
from utils.settings import settings
from core.logic.collect_tickets import handle_tickets
from core.capture import get_bbs_screenshot
from core.logic.handle_gameplay_single_player import handle_gameplay_single_player
from core.logic.end_menu_singleplayer import handle_end_menu_singleplayer

def sub_stories():
    stop_controller.reset() 
    
    banner = prepare_game_execution(lambda: stop_controller.stop())
    if not banner:
        return "Game window not found. Please make sure the game is open and properly positioned."
    
    start_esc_listener(lambda: (
        stop_controller.stop(),
        banner.close()
    ))
    
    while not stop_controller.should_stop():
        screenshot = get_bbs_screenshot()
        
        # Check if we're on the main sub stories menu
        if check_image_present("assets/icons/sub_stories_title.png", screenshot=screenshot):
            debug("[Sub Stories] On main sub stories menu - looking for NEW icon")
            
            # Look for any NEW icon on the screen
            if check_image_present("assets/icons/new.png", screenshot=screenshot):
                debug("[Sub Stories] Found NEW icon, clicking on sub story")
                
                # Click on the NEW icon to enter the sub story
                if find_and_click_image("assets/icons/new.png", screenshot=screenshot):
                    time.sleep(2)
                    debug("[Sub Stories] Entered sub story, checking all pages")
                    
                    # Go through all pages of this sub story
                    page = 1
                    max_pages = 5  # Reasonable limit
                    
                    while page <= max_pages and not stop_controller.should_stop():
                        screenshot = get_bbs_screenshot()
                        debug(f"[Sub Stories] Checking page {page}")
                        
                        # Look for NEW stories on current page
                        if check_image_present("assets/icons/new.png", screenshot=screenshot):
                            debug(f"[Sub Stories] Found NEW story on page {page}")
                            
                            # Click on the NEW story
                            if find_and_click_image("assets/icons/new.png", screenshot=screenshot):
                                time.sleep(1)
                                
                                # Handle the story completion
                                handle_sub_story_quest()

                                continue  # Check the same page again for more NEW stories
                            else:
                                debug("[Sub Stories] Could not click on NEW story")
                                return "Found NEW story but could not click on it"
                        else:
                            debug(f"[Sub Stories] No NEW stories on page {page}")
                            
                            # Try to go to next page
                            if page < max_pages:
                                # Click next page button (page number)
                                if find_and_click_image(f"assets/icons/sub_{page + 1}.png", screenshot=screenshot, threshold=0.9):
                                    page += 1
                                    time.sleep(1)
                                    debug(f"[Sub Stories] Moved to page {page}")
                                else:
                                    debug(f"[Sub Stories] No more pages in this sub story")
                                    break
                            else:
                                debug(f"[Sub Stories] Reached max pages limit")
                                break
                        
                        if stop_controller.should_stop():
                            break
                            
                    # Go back to main sub stories menu
                    screenshot = get_bbs_screenshot()
                    find_and_click_image("assets/icons/back.png", screenshot=screenshot)
                    time.sleep(1)
                    debug("[Sub Stories] Back to main menu, restarting loop")
                    
                else:
                    debug("[Sub Stories] Could not click on NEW sub story")
                    return "Found NEW sub story but could not click on it"
            else:
                debug("[Sub Stories] No NEW sub stories found")
                return "No NEW sub stories found to complete"
                
        else:
            debug("[Sub Stories] Not on main sub stories menu")
            return "Not on main sub stories menu"

        # Check for stop condition before sleep
        if stop_controller.should_stop():
            break
            
        quest_completed = False
        time.sleep(2)
   
    stop_controller.stop()
    banner.close()
    return True

def handle_sub_story_quest():
    """Handle the completion of a single sub story quest."""
    debug("[Sub Story Quest] Starting quest selection")
    
    quest_completed = False
    
    while not stop_controller.should_stop():
        screenshot = get_bbs_screenshot()
        
        # Check if we're on the quest selection screen 
        if check_image_present("assets/icons/new_2.png", screenshot=screenshot):
            debug("[Sub Story Quest] Found NEW quest, clicking on it")
            if find_and_click_image("assets/icons/new_2.png", screenshot=screenshot):
                time.sleep(1)
                debug("[Sub Story Quest] Clicked on NEW quest")
        
        # Check for ok button (story only) 
        elif check_image_present("assets/icons/ok.png", screenshot=screenshot):
            debug("[Sub Story Quest] Found ok button")
            if find_and_click_image("assets/icons/ok.png", screenshot=screenshot):
                time.sleep(1)
                debug("[Sub Story Quest] Clicked ok")
                
        # handle skip on story only 
        elif check_image_present("assets/icons/skip.png", screenshot=screenshot):
            find_and_click_image("assets/icons/skip.png", screenshot=screenshot)
        
        # Check for quest clear button
        elif check_image_present("assets/icons/quest_clear.png", screenshot=screenshot):
            debug("[Sub Story Quest] Found quest clear button")
            if find_and_click_image("assets/icons/quest_clear.png", screenshot=screenshot):
                time.sleep(1)
                debug("[Sub Story Quest] Clicked quest clear")
        
        # Check for prepare for quest button
        elif check_image_present("assets/icons/prepare_for_quest.png", screenshot=screenshot):
            debug("[Sub Story Quest] Found prepare for quest button")
            if find_and_click_image("assets/icons/prepare_for_quest.png", screenshot=screenshot):
                time.sleep(1)
                debug("[Sub Story Quest] Clicked prepare for quest")
        
        # Check for start quest button
        elif check_image_present("assets/icons/start_quest.png", screenshot=screenshot):
            debug("[Sub Story Quest] Found start quest button")
            if find_and_click_image("assets/icons/start_quest.png", screenshot=screenshot):
                time.sleep(1)
                screenshot = get_bbs_screenshot()
                find_and_click_image("assets/icons/ok.png", screenshot=screenshot)
                debug("[Sub Story Quest] Started quest")
        
        # Check if in gameplay
        elif check_image_present("assets/icons/pause.png", screenshot=screenshot):
            debug("[Sub Story Quest] In gameplay")
            handle_gameplay_single_player()
            handle_end_menu_singleplayer()
        

        # Check for close button (no more NEW quests in this story)
        elif check_image_present("assets/icons/close.png", screenshot=screenshot):
            debug("[Sub Story Quest] No more NEW quests found, clicking close")
            if find_and_click_image("assets/icons/close.png", screenshot=screenshot):
                time.sleep(1)
                debug("[Sub Story Quest] Closed story, returning to page")
                return True  # Successfully completed all quests in this story
        
        time.sleep(1)
    
    return quest_completed