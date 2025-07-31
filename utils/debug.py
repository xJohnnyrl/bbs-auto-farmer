import os
import subprocess
from utils.logger import debug

debug_process = None

def open_debug_terminal():
    global debug_process

    from utils.logger import log_path  # use the dynamic path
    debug_process = subprocess.Popen(
        [
            "powershell.exe", "-NoLogo", "-NoProfile", "-Command", 
            f'Get-Content "{log_path}" -Wait'
        ],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    debug("Debug mode started")

def close_debug_terminal():
    global debug_process
    if debug_process and debug_process.poll() is None:
        debug_process.terminate()