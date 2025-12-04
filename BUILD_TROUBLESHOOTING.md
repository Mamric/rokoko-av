# Building the Executable - Troubleshooting Guide

## PyInstaller Installation Issues on Windows

If you encounter errors when installing PyInstaller, try these solutions in order:

### Solution 1: Run as Administrator (Most Common Fix)

1. **Close your current terminal/PowerShell**
2. **Right-click on PowerShell or Command Prompt**
3. **Select "Run as administrator"**
4. **Navigate to your project directory**:
   ```powershell
   cd "C:\Users\nicky\Desktop\rokoko audio video"
   ```
5. **Try installing again**:
   ```powershell
   pip install pyinstaller
   ```

### Solution 2: Install with --user Flag

This installs PyInstaller in your user directory instead of the system Python directory:

```powershell
pip install --user pyinstaller
```

Note: After using `--user`, you may need to add the user scripts directory to your PATH, or use:
```powershell
python -m PyInstaller --onefile --windowed rokoko_av.py
```

### Solution 3: Force Reinstall with Clean Cache

```powershell
pip install --force-reinstall --no-cache-dir pyinstaller
```

### Solution 4: Close Python Processes

Sometimes Python processes lock files. Try:

1. **Close all Python applications** (IDEs, Jupyter notebooks, etc.)
2. **Open Task Manager** (Ctrl+Shift+Esc)
3. **End any Python processes** you see
4. **Try installing again**

### Solution 5: Install Specific Version

Sometimes a specific version works better:

```powershell
pip install pyinstaller==6.3.0
```

### Solution 6: Use Virtual Environment

Create an isolated environment to avoid conflicts:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Now PyInstaller should install cleanly
pip install pyinstaller
```

### Solution 7: Manual File Cleanup (Advanced)

If files are truly locked, you may need to:

1. Close all Python processes
2. Delete the problematic file manually:
   ```powershell
   # Run PowerShell as Administrator first!
   Remove-Item "C:\Python312\Scripts\pyi-archive_viewer.exe.deleteme" -Force -ErrorAction SilentlyContinue
   Remove-Item "C:\Python312\Scripts\pyi-archive_viewer.exe" -Force -ErrorAction SilentlyContinue
   ```
3. Try installing again

### Solution 8: Check Antivirus/Security Software

Some antivirus software blocks PyInstaller installation. Temporarily disable it or add Python to exclusions.

## Alternative: Use Python Module Directly

If PyInstaller installs but `pyinstaller` command doesn't work, you can use it as a Python module:

```powershell
python -m PyInstaller --onefile --windowed --name=rokoko-av-recorder --clean rokoko_av.py
```

This works even if the command-line tools aren't in your PATH.

## Verify Installation

After installation, verify it works:

```powershell
pyinstaller --version
# OR
python -m PyInstaller --version
```

## Still Having Issues?

If none of these work, you can:
1. Use the GUI application directly with Python: `python rokoko_av.py`
2. Create a batch file to launch it easily
3. Check Python installation for corruption: `python -m pip install --upgrade pip`


