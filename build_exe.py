"""
Helper script to build the Rokoko Audio/Video Recorder into a standalone .exe file.

Usage:
    python build_exe.py
    
This will create a single-file executable in the 'dist' directory.
"""

import subprocess
import sys
import os

def build_exe():
    """Build the executable using PyInstaller."""
    
    script_path = os.path.join(os.path.dirname(__file__), "rokoko_av.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Could not find {script_path}")
        sys.exit(1)
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create a single-file executable
        "--windowed",                   # No console window (GUI only)
        "--name=rokoko-av-recorder",    # Name of the executable
        "--icon=NONE",                  # No icon (can add .ico file later)
        "--clean",                      # Clean PyInstaller cache before building
        script_path
    ]
    
    print("Building executable with PyInstaller...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True)
        print()
        print("=" * 60)
        print("Build completed successfully!")
        print("=" * 60)
        print(f"\nExecutable location: dist/rokoko-av-recorder.exe")
        print("\nNote: The first run may be slower as Windows needs to extract the files.")
        print("      The executable can be run directly without Python installed.")
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("Build failed!")
        print("=" * 60)
        print(f"\nError: {e}")
        print("\nMake sure PyInstaller is installed:")
        print("  pip install pyinstaller")
        sys.exit(1)
    except FileNotFoundError:
        print()
        print("=" * 60)
        print("Error: PyInstaller not found!")
        print("=" * 60)
        print("\nPlease install PyInstaller first:")
        print("  pip install pyinstaller")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()


