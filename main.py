from gui.main_window import run
from utils.debug import open_debug_terminal
from utils.settings import settings


if __name__ == "__main__":
    if settings["debug_mode"]:
        open_debug_terminal()
    run()