# BBS Auto Farmer

An automated farming tool for Bleach: Brave Souls that can handle various game modes including quests, co-op, epic raids, sub stories, and PvP battles.

## Features

- **Retry Stage**: Automate story quest retries with orb/ticket management
- **Co-Op Quests**: Automated co-op quest farming
- **Epic Raid**: Automated epic raid participation
- **Special Moves**: Automated special moves training
- **Sub Stories**: Complete sub stories with NEW quest detection
- **Brave Battles**: Automated PvP battles
- **Smart Settings**: Configurable limits for orbs, tickets, and battles
- **Error Handling**: Custom error messages and graceful failure handling
- **ESC to Stop**: Press ESC at any time to stop the automation

## Prerequisites

- **Python 3.11+**
- **Windows 10/11** (uses Windows-specific window management)
- **Bleach: Brave Souls** game client
- **Game Resolution**: 1600x900 (required for image recognition)

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

### 3. Alternative: Using pip

```bash
pip install -r requirements.txt
```

## Building Executable

### Option 1: Using the Build Script (Recommended)

```bash
python build_installer.py
```

This will automatically install PyInstaller if needed and create both the executable and installer.

### Option 2: Manual PyInstaller Build

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable (no console window)
pyinstaller --noconsole --onefile --name=bbs_auto_farmer --add-data="assets/icons;assets/icons" --add-data="config;config" --add-data="gui/style.qss;gui" main.py
```

### Option 3: Using the Spec File

```bash
pyinstaller bbs_auto_farmer.spec
```

### Executable Location

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
# Activate virtual environment (if using uv)
uv run python main.py

# Or directly with Python
python main.py
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

### Automation Features

#### Smart Image Recognition

- **Top-Left Priority**: Always clicks the most top-left occurrence of UI elements
- **Error Handling**: Custom error messages for different failure scenarios
- **Graceful Stops**: ESC key stops automation at any point

#### Game Mode Specific Features

**Sub Stories**:

- Detects NEW icons on sub story categories
- Navigates through all pages of each sub story
- Completes all NEW quests within each story
- Returns to main menu when done

**Brave Battles**:

- Simple battle loop with configurable limits
- Handles battle completion and return to PvP screen

**Other Modes**:

- Orb and ticket management
- Boost automation
- Revive candle usage
- Giftbox ticket collection

## Troubleshooting

### Common Issues

1. **"Game window not found"**

   - Ensure Bleach: Brave Souls is running
   - Check that the window is not minimized
   - Verify the game resolution is 1600x900

2. **"Not on [specific] screen"**

   - Navigate to the correct menu before starting automation
   - For Sub Stories: Go to Sub Stories menu
   - For Brave Battles: Go to PvP screen

3. **Image recognition failures**

   - Check that game UI hasn't changed
   - Verify screen resolution is correct
   - Ensure game window is fully visible

4. **ESC not stopping automation**
   - Wait for current action to complete
   - Try pressing ESC multiple times
   - Check if debug terminal shows stop messages

### Debug Mode

Enable debug mode in settings to see detailed logs:

- Shows current automation state
- Displays image recognition attempts
- Logs all clicks and actions
- Helps identify issues

## Development

### Adding New Game Modes

1. Create a new file in `core/logic/`
2. Implement the automation logic
3. Add GUI button in `gui/main_window.py`
4. Add any required icon assets to `assets/icons/`

### Icon Assets

The application uses image recognition for UI automation. To add new functionality:

1. Capture screenshots of UI elements
2. Save as PNG files in `assets/icons/`
3. Reference in code using `check_image_present()` and `find_and_click_image()`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/xJohnnyrl/bbs-auto-farmer/issues)
- **Twitter**: [@xJohnnyrl](https://x.com/xJohnnyrl)
- **YouTube**: Tutorial coming soon

## License

This project is for educational purposes. Use at your own risk and in accordance with the game's terms of service.

## Disclaimer

This tool is designed for automation of repetitive tasks in Bleach: Brave Souls. Use responsibly and in accordance with the game's terms of service. The developers are not responsible for any consequences of using this tool.
