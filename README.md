# BBS Auto Farmer

An automated farming tool for Bleach: Brave Souls that can handle various game modes including point events, co-op, epic raids, sub stories, and brave battles.

Check out the [tutorial](https://youtu.be/5Iqe13ydSzs?si=IZm7LfMLiDGNbXct) on how to get started

## Features

- **Retry Stage**: Automate story quest retries with orb/ticket management
- **Co-Op Quests**: Automated co-op quest farming
- **Epic Raid**: Automated epic raid participation
- **Special Moves**: Automated special moves training
- **Sub Stories**: Complete sub stories with NEW quest detection
- **Brave Battles**: Automated PvP battles
- **Smart Settings**: Configurable limits for orbs, tickets, and battles

- **Python**
- **uv**

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/xJohnnyrl/bbs-auto-farmer.git
cd bbs-auto-farmer
```

### 2. Install Dependencies

This project uses `uv` for dependency management. Install it first:

```bash
# Install uv (if not already installed)
pip install uv

# Install project dependencies
uv sync
```

## Building Executable

### Using the Build Script (Recommended)

```bash
python build_installer.py
```

This will automatically install PyInstaller if needed and create both the executable and installer.

After building, the executable will be located at:

- `dist/bbs_auto_farmer.exe`

### Executable Behavior

When running the executable:

- **No Console Window**: Runs silently in the background
- **Logs**: Will be created in `AppData/BBS Auto Farmer/logs/`
- **Config**: Will be created in `AppData/BBS Auto Farmer/config/`
- **Assets**: Are bundled within the executable
- **Debug Mode**: Can be enabled in settings to show console window

## Creating Installer

### Using Inno Setup

1. **Install Inno Setup**: Download from https://jrsoftware.org/isinfo.php
2. **Build Installer**: Run the build script or manually:

   ```bash
   # Using build script (automatically detects Inno Setup)
   python build_installer.py

   # Manual Inno Setup compilation
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
   ```

### Installer Features

- **Silent Installation**: No console window during installation
- **AppData Storage**: Logs and config stored in user's AppData directory
- **Desktop Shortcut**: Optional desktop icon creation
- **Start Menu**: Adds to Windows Start Menu
- **Uninstaller**: Proper cleanup on uninstall

## Project Structure

```
bbs-auto-farmer/
├── main.py                 # Application entry point
├── pyproject.toml         # Project configuration and dependencies
├── uv.lock               # Locked dependency versions
├── .python-version       # Python version specification
├── config/
│   └── user_settings.json # User configuration file
├── assets/
│   └── icons/            # Image recognition assets
│       ├── new.png       # NEW icon detection
│       ├── start_quest.png # Start quest button
│       ├── pause.png     # Pause button detection
│       └── ...           # Various UI element images
├── core/
│   ├── actions.py        # Image recognition and clicking
│   ├── capture.py        # Screenshot capture utilities
│   ├── window_utils.py   # Window management
│   ├── esc_listener.py   # ESC key listener
│   ├── stop_controller.py # Stop mechanism
│   ├── state.py          # Game state management
│   └── logic/            # Game mode automation logic
│       ├── retry_stage.py # Retry stage automation
│       ├── co_op.py      # Co-op quest automation
│       ├── epic_raid.py  # Epic raid automation
│       ├── retry_special_moves.py # Special moves automation
│       ├── sub_stories.py # Sub stories automation
│       ├── brave_battles.py # PvP automation
│       ├── gameplay.py   # General gameplay handling
│       ├── end_menu.py   # End menu handling
│       └── ...           # Other game logic modules
├── gui/
│   ├── main_window.py    # Main GUI application
│   └── style.qss         # GUI styling
└── utils/
    ├── settings.py       # Settings management
    ├── logger.py         # Logging utilities
    ├── debug.py          # Debug terminal
    └── logs/             # Log files directory
```

## Configuration

### Settings File

Edit `config/user_settings.json` to configure the automation:

```json
{
  "max_orbs": 0, // Max orbs to use (0 = wait for tickets)
  "max_tickets": 10, // Max tickets to use (-1 = infinite)
  "use_revive_candles": true, // Use revive candles when needed
  "auto_set_boost_to_max": true, // Auto-set boost to maximum
  "auto_collect_ticket_from_giftbox": false, // Auto-collect tickets
  "debug_mode": true, // Enable debug terminal
  "brave_battles_tickets": 5 // Number of PvP battles to complete
}
```

### Game Setup

1. **Resolution**: Set Bleach: Brave Souls to 1600x900
2. **Window Position**: Ensure the game window is visible and not minimized
3. **Game State**: Navigate to the appropriate menu before starting automation

## Usage

### Running the Application

```bash
# Activate virtual environment
uv run python main.py
```

### GUI Interface

The application provides a user-friendly GUI with three tabs:

#### Main Tab

- **Start Retry Quest**: Automate story quest retries
- **Start Co-Op Quest**: Automate co-op quests
- **Start Epic Raid**: Automate epic raids (not recommended)
- **Start Special Moves**: Automate special moves training
- **Start Sub Stories**: Automate sub story completion
- **Start Brave Battles**: Automate PvP battles

#### Settings Tab

- **Max Orbs**: Limit orb usage
- **Max Tickets**: Limit ticket usage
- **Use Revive Candles**: Enable/disable revive candles
- **Debug Mode**: Enable debug terminal
- **Auto Boost to Max**: Automatically set boost to maximum
- **Auto Collect Tickets**: Automatically collect tickets from giftbox
- **Brave Battles Tickets**: Number of PvP battles to complete

#### Info Tab

- **GitHub Repository**: Source code and issues
- **YouTube Tutorial**: Video guide (coming soon)
- **Feedback**: Submit issues or contact via Twitter

### Debug Mode

Enable debug mode in settings to see detailed logs:

- Shows current automation state
- Displays image recognition attempts
- Logs all clicks and actions
- Helps identify issues

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/xJohnnyrl/bbs-auto-farmer/issues)
- **Twitter**: [@xJohnnyrl](https://x.com/xJohnnyrl)
- **YouTube**: Tutorial coming soon

## License

This project is for educational purposes. Use at your own risk and in accordance with the game's terms of service.

## Disclaimer

This tool is designed for automation of repetitive tasks in Bleach: Brave Souls. Use responsibly and in accordance with the game's terms of service. The developers are not responsible for any consequences of using this tool.
