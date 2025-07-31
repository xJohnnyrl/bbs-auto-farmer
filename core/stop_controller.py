import threading

class StopController:
    def __init__(self):
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def should_stop(self):
        return self._stop_event.is_set()

    def reset(self):
        self._stop_event.clear()

stop_controller = StopController()