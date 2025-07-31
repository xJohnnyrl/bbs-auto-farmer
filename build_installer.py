#!/usr/bin/env python3
"""
Build script for BBS Auto Farmer
Creates PyInstaller executable and optionally Inno Setup installer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller version: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        return True

def check_inno_setup():
    """Check if Inno Setup is available"""
    inno_compiler = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if os.path.exists(inno_compiler):
        print(f"✓ Inno Setup found: {inno_compiler}")
        return inno_compiler
    else:
        print("✗ Inno Setup not found. Install from: https://jrsoftware.org/isinfo.php")
        print("  Installer will be created manually using installer.iss")
        return None

def clean_build():
    """Clean previous builds"""
    print("Cleaning previous builds...")
    for path in ["build", "dist"]:
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                print(f"  Removed {path}/")
            except PermissionError:
                print(f"  Warning: Could not remove {path}/ (files may be in use)")
                # Try to remove individual files that aren't locked
                try:
                    for root, dirs, files in os.walk(path, topdown=False):
                        for name in files:
                            try:
                                os.remove(os.path.join(root, name))
                            except PermissionError:
                                pass
                        for name in dirs:
                            try:
                                os.rmdir(os.path.join(root, name))
                            except PermissionError:
                                pass
                except Exception:
                    pass

def build_executable():
    """Build the PyInstaller executable"""
    print("Building executable...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",  # Hide console window
        "--onefile",
        "--name=bbs_auto_farmer",
        "--add-data=assets/icons;assets/icons",
        "--add-data=config;config", 
        "--add-data=gui/style.qss;gui",
        "--hidden-import=cv2",
        "--hidden-import=numpy",
        "--hidden-import=pyautogui",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageTk",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.messagebox",
        "main.py"
    ]
    
    result = subprocess.run(cmd, check=True)
    
    if result.returncode == 0:
        print("✓ Executable built successfully!")
        print(f"  Location: dist/bbs_auto_farmer.exe")
        return True
    else:
        print("✗ Build failed!")
        return False

def build_installer(inno_compiler):
    """Build the Inno Setup installer"""
    if not inno_compiler:
        print("⚠ Inno Setup not available. Manual build required:")
        print("  1. Install Inno Setup from https://jrsoftware.org/isinfo.php")
        print("  2. Run: ISCC.exe installer.iss")
        return False
    
    print("Building installer...")
    
    # Create installer directory
    installer_dir = "installer"
    os.makedirs(installer_dir, exist_ok=True)
    
    # Run Inno Setup compiler
    cmd = [inno_compiler, "installer.iss"]
    result = subprocess.run(cmd, check=True)
    
    if result.returncode == 0:
        print("✓ Installer built successfully!")
        print(f"  Location: installer/bbs_auto_farmer_setup.exe")
        return True
    else:
        print("✗ Installer build failed!")
        return False

def main():
    print("BBS Auto Farmer - Build Script")
    print("=" * 40)
    
    # Check dependencies
    if not check_pyinstaller():
        return False
    
    inno_compiler = check_inno_setup()
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    if not build_executable():
        return False
    
    # Build installer (optional)
    if inno_compiler:
        build_installer(inno_compiler)
    
    print("\n" + "=" * 40)
    print("Build completed!")
    print("\nFiles created:")
    print(f"  - Executable: dist/bbs_auto_farmer.exe")
    if inno_compiler:
        print(f"  - Installer: installer/bbs_auto_farmer_setup.exe")
    
    print("\nNotes:")
    print("  - Executable will create logs/config in AppData/BBS Auto Farmer/")
    print("  - Debug mode can be enabled in settings to show console")
    print("  - All assets are bundled within the executable")
    
    return True

if __name__ == "__main__":
    main() 