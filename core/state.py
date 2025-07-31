from enum import Enum
from utils.logger import debug

class GameState(Enum):
    MENU = "menu"
    IN_GAME = "in_game"
    LOADING = "loading"
    ERROR = "error"
    END_GAME = "end_menu"

class AppState:
    def __init__(self):
        self.state = GameState.MENU

    def set(self, new_state: GameState):
        debug(f"[STATE] Transition: {self.state.value} → {new_state.value}")
        self.state = new_state

    def get(self) -> GameState:
        return self.state


# Singleton instance you can import
state = AppState()
