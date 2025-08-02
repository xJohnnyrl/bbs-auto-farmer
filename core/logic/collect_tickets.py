from utils.settings import settings
from utils.logger import debug
from core.actions import find_and_click_image, check_image_present
import time
from core.capture import get_bbs_screenshot

def handle_tickets(orbs, max_orbs, multiplayer=False):
    if settings["auto_collect_ticket_from_giftbox"] and not multiplayer:
        debug("[Tickets] Auto collecting ticket from giftbox.")
        find_and_click_image("assets/icons/cancel.png")
        time.sleep(1)
        find_and_click_image("assets/icons/menu.png", threshold=0.6)
        time.sleep(1)
        find_and_click_image("assets/icons/giftbox.png")
        time.sleep(3)
        find_and_click_image("assets/icons/menu_soul_ticket.png")
        time.sleep(1)
        if (check_image_present("assets/icons/no_gifts_left.png")):
            debug("[Tickets] No gifts left.")
            find_and_click_image("assets/icons/close.png")
            time.sleep(1)
            find_and_click_image("assets/icons/start_quest.png")
            orbs = handle_tickets_with_orbs(orbs, max_orbs)
            return orbs
        find_and_click_image("assets/icons/collect_tickets.png")
        time.sleep(1)
        find_and_click_image("assets/icons/ok.png")
        time.sleep(1)
        find_and_click_image("assets/icons/close.png")
        time.sleep(1)
        find_and_click_image("assets/icons/close.png")
    elif settings["auto_collect_ticket_from_giftbox"] and multiplayer:
        debug("[Tickets] Auto collecting ticket from giftbox.")
        find_and_click_image("assets/icons/co_op_gift_box.png")
        time.sleep(3)
        find_and_click_image("assets/icons/menu_soul_ticket.png")
        time.sleep(1)
        if (check_image_present("assets/icons/no_gifts_left.png")):
            debug("[Tickets] No gifts left.")
            find_and_click_image("assets/icons/close.png")
            time.sleep(1)
            find_and_click_image("assets/icons/start_quest.png")
            orbs = handle_tickets_with_orbs(orbs, max_orbs, multiplayer)
            return orbs
        find_and_click_image("assets/icons/collect_tickets.png")
        time.sleep(1)
        find_and_click_image("assets/icons/ok.png")
        time.sleep(1)
        find_and_click_image("assets/icons/close.png")
        time.sleep(1)
        find_and_click_image("assets/icons/close.png")
        time.sleep(1)
        find_and_click_image("assets/icons/close.png")
    else:
        orbs = handle_tickets_with_orbs(orbs, max_orbs, multiplayer)

    return orbs

def handle_tickets_with_orbs(orbs, max_orbs, multiplayer=False):
    if (max_orbs == 0):
        return orbs
    
    if multiplayer:
        find_and_click_image("assets/icons/close.png")
        time.sleep(1)
        find_and_click_image("assets/icons/buy.png")
        time.sleep(0.5)
        find_and_click_image("assets/icons/50_soul_tickets.png", top_left=False)
        time.sleep(1)
        find_and_click_image("assets/icons/purchase.png")
        time.sleep(1)
        find_and_click_image("assets/icons/close.png")
    else:
        debug("[Tickets] Using Orbs to buy tickets.")
        find_and_click_image("assets/icons/purchase.png")
        time.sleep(0.5)
        find_and_click_image("assets/icons/50_soul_tickets.png", top_left=False)
        time.sleep(1)
        find_and_click_image("assets/icons/purchase.png")
        time.sleep(1)
        find_and_click_image("assets/icons/close.png")
    
    orbs += 10 
    return orbs