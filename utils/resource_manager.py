import os
import sys
from pathlib import Path

def get_resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource file.
    Works both in development and when bundled with PyInstaller.
    
    Args:
        relative_path: Path relative to the project root (e.g., "assets/icons/auto_off.png")
        
    Returns:
        Absolute path to the resource file
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Not running in PyInstaller, use the current directory
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def get_asset_path(asset_name: str) -> str:
    """
    Get the path to an asset file in the assets directory.
    
    Args:
        asset_name: Name of the asset file (e.g., "auto_off.png")
        
    Returns:
        Absolute path to the asset file
    """
    return get_resource_path(f"assets/icons/{asset_name}")

def get_logs_directory() -> str:
    """
    Get the directory for log files.
    In development: utils/logs/
    In PyInstaller: user's AppData directory
    
    Returns:
        Path to the logs directory
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        # Use user's AppData directory for logs when bundled
        appdata_dir = os.path.join(os.getenv('APPDATA', os.path.expanduser("~")), "BBS Auto Farmer")
        logs_dir = os.path.join(appdata_dir, "logs")
    except Exception:
        # Not running in PyInstaller, use the project's logs directory
        logs_dir = os.path.join(os.path.abspath("."), "utils", "logs")
    
    # Ensure the logs directory exists
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir

def get_config_directory() -> str:
    """
    Get the directory for configuration files.
    In development: config/
    In PyInstaller: user's AppData directory
    
    Returns:
        Path to the config directory
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        # Use user's AppData directory for config when bundled
        appdata_dir = os.path.join(os.getenv('APPDATA', os.path.expanduser("~")), "BBS Auto Farmer")
        config_dir = os.path.join(appdata_dir, "config")
    except Exception:
        # Not running in PyInstaller, use the project's config directory
        config_dir = os.path.join(os.path.abspath("."), "config")
    
    # Ensure the config directory exists
    os.makedirs(config_dir, exist_ok=True)
    return config_dir 