import cv2
import numpy as np
import pyautogui
import os
from core.capture import get_bbs_screenshot
import time
from utils.resource_manager import get_asset_path

def check_image_present(template_path: str, screenshot=None, threshold: float = 0.85) -> bool:
    if screenshot is None:
        screenshot = get_bbs_screenshot()

    # Handle asset paths (e.g., "auto_off.png") or full paths
    if not os.path.isabs(template_path) and not template_path.startswith("assets/"):
        # Assume it's an asset name
        template_path = get_asset_path(template_path)
    elif template_path.startswith("assets/"):
        # Handle full asset paths
        from utils.resource_manager import get_resource_path
        template_path = get_resource_path(template_path)

    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template not found: {template_path}")

    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    return max_val >= threshold


def find_and_click_image(template_path: str, screenshot=None, threshold: float = 0.85, double_click: bool = False, top_left: bool = True) -> bool:
    from core.window_utils import get_bbs_window

    if screenshot is None:
        screenshot = get_bbs_screenshot()

    win = get_bbs_window()

    # Handle asset paths (e.g., "auto_off.png") or full paths
    if not os.path.isabs(template_path) and not template_path.startswith("assets/"):
        # Assume it's an asset name
        template_path = get_asset_path(template_path)
    elif template_path.startswith("assets/"):
        # Handle full asset paths
        from utils.resource_manager import get_resource_path
        template_path = get_resource_path(template_path)

    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template not found: {template_path}")

    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    
    # Find all locations where the template matches above threshold
    locations = np.where(res >= threshold)
    locations = list(zip(*locations[::-1]))  # Convert to (x, y) format
    
    if not locations:
        return False
    
    if top_left:
        # Sort by y-coordinate first (top to bottom), then by x-coordinate (left to right)
        # This ensures we get the most top-left match
        locations.sort(key=lambda loc: (loc[1], loc[0]))
        max_loc = locations[0]
    else:
        # Find the location with the highest confidence (most accurate match)
        max_val = 0
        max_loc = None
        for loc in locations:
            val = res[loc[1], loc[0]]
            if val > max_val:
                max_val = val
                max_loc = loc
        
        if max_loc is None:
            return False
    
    max_val = res[max_loc[1], max_loc[0]]

    h, w = template.shape[:2]
    center_x = max_loc[0] + w // 2
    center_y = max_loc[1] + h // 2

    global_x = win.left + center_x
    global_y = win.top + center_y

    if double_click:
        pyautogui.click(global_x, global_y)
        time.sleep(0.5)
        pyautogui.click(global_x, global_y)
    else:
        pyautogui.click(global_x, global_y)
    return True