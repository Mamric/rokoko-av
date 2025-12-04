# Rokoko Audio Video Sync Recorder

A GUI application that synchronously records motion capture data from Rokoko Studio and audio from Audacity, allowing you to capture both simultaneously with a single button click.

## Features

- **GUI Interface**: Simple and intuitive graphical interface with Record/Stop button
- **Synchronized Recording**: Start and stop both Rokoko mocap and Audacity audio recording simultaneously
- **Real-time Logging**: Built-in log window showing recording status and messages
- **Settings Management**: Configure Rokoko connection settings through the GUI
- **Persistent Application**: Keep the application running and record multiple times without restarting
- **Continuous Recording**: Continue recording on the same Audacity track across multiple recordings
- **No Auto-Save**: You maintain full control over when and how to save your Audacity projects

## Prerequisites

Before setting up this script, ensure you have the following installed and configured:

### Required Software

1. **Python 3.7+** 
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Rokoko Studio**
   - Download from [Rokoko website](https://www.rokoko.com/)
   - Ensure the API is enabled and accessible

3. **Audacity 3.7.5+**
   - Download from [Audacity website](https://www.audacityteam.org/)
   - **Important**: Must have `mod-script-pipe` module enabled (see setup instructions below)

## Installation

### 1. Clone or Download This Repository

```bash
git clone <your-repo-url>
cd rokoko-audio-video
```

Or download and extract the ZIP file to your desired location.

### 2. Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests pyaudacity-x
```

**Note**: The script uses `pyaudacity-x` which has better Windows support than the standard `pyaudacity` package.

### 3. Set Up Configuration (Optional)

The application will create a default `config.json` file on first run. If you want to pre-configure settings:

1. Copy the example config file:
   ```bash
   copy config.json.example config.json
   ```

2. Edit `config.json` with your Rokoko Studio settings, or configure them later through the GUI Settings window.

See `CONFIG_TEMPLATE.md` for detailed configuration information.

### 4. Configure Audacity

1. **Open Audacity**

2. **Enable mod-script-pipe Module**:
   - Go to `Edit → Preferences → Modules`
   - Find `mod-script-pipe` in the list
   - Set it to **Enabled** (not "New" or "Disabled")
   - Click **OK**

3. **Restart Audacity** (required for the module to load)

4. **Verify Audio Device Settings**:
   - Go to `Edit → Preferences → Devices`
   - Ensure your recording device (microphone) is selected
   - Set appropriate input levels

5. **Keep Audacity Running**: The script requires Audacity to be running before you execute it

### 5. Configure Rokoko Studio

1. **Open Rokoko Studio**

2. **Enable API Access**:
   - Ensure the API is enabled in Rokoko Studio settings
   - Note your API key (default is usually "1234")

3. **Verify Network Settings**:
   - Check the IP address and port where Rokoko Studio is running
   - Default port is usually `14053`

## Configuration

Configuration is managed through the Settings window in the GUI application. Click the **Settings** button in the main window to configure:

- **Rokoko IP Address**: The IP address where Rokoko Studio is running
- **Rokoko Port**: The port for Rokoko API (default: 14053)
- **Rokoko API Key**: Your Rokoko API key (default: "1234")
- **Clip Name**: Name for your Rokoko recordings
- **Frame Rate**: Frame rate for mocap recording (default: 60)

Settings are automatically saved to `config.json` in the application directory.

**Note**: `config.json` is not tracked in git (it's in `.gitignore`) since it contains user-specific settings. Each user should configure their own settings through the Settings window.

### Setting Up Configuration

You can set up your configuration in two ways:

1. **Through the GUI** (Recommended): Click the **Settings** button in the application and configure your settings there.

2. **Manually**: Copy `config.json.example` to `config.json` and edit it:
   ```bash
   copy config.json.example config.json
   ```
   See `CONFIG_TEMPLATE.md` for detailed information about each configuration field.

### Finding Your Rokoko IP Address

- If Rokoko Studio is on the same computer: Use `127.0.0.1` or `localhost`
- If Rokoko Studio is on a different computer: Use that computer's local IP address (e.g., `192.168.0.163`)

## Usage

1. **Start Rokoko Studio** and ensure it's ready to record

2. **Start Audacity** and ensure:
   - `mod-script-pipe` is enabled (see Installation step 3)
   - Your audio device is configured
   - Audacity is running (don't close it)

3. **Run the Application**:
   
   **Option A: Run from Python**
   ```bash
   python rokoko_av.py
   ```
   
   **Option B: Run the Executable** (if you've built it)
   ```bash
   dist/rokoko-av-recorder.exe
   ```

4. **Configure Settings** (if needed):
   - Click the **Settings** button in the application window
   - Enter your Rokoko IP address, port, API key, and other settings
   - Click **Save**

5. **Start Recording**:
   - Click the large **RECORD** button
   - Both Rokoko and Audacity will begin recording simultaneously
   - The button will change to **STOP** and turn red
   - Status will show "Recording..." in red

6. **Stop Recording**:
   - Click the **STOP** button when you're done
   - Both recordings will stop simultaneously
   - Status will return to "Ready" in green

7. **View Logs**:
   - All recording activity is logged in the log window at the bottom
   - Scroll through the log to see detailed information about each operation

8. **Save Your Work**:
   - **Rokoko**: Check Rokoko Studio for your mocap file
   - **Audacity**: Manually save your project (`File → Save Project`)

### Multiple Recordings

The application is designed to continue recording on the same Audacity track across multiple recording sessions. Simply click **RECORD** again to start another recording, and it will append to your existing audio track instead of creating new ones. You can record multiple times without closing the application.

## Troubleshooting

### "Cannot connect to Audacity" Error

- **Solution**: Make sure Audacity is running and `mod-script-pipe` is enabled
- Verify: `Edit → Preferences → Modules` → `mod-script-pipe` should show "Enabled"
- **Important**: Restart Audacity after enabling the module

### "Error starting Rokoko" Error

- **Solution**: Check that:
  - Rokoko Studio is running
  - The IP address and port in the script match your Rokoko Studio settings
  - The API key is correct
  - Your network connection is working

### Recording Not Starting in Audacity

- **Check Audio Device**: `Edit → Preferences → Devices` → Verify recording device is selected
- **Check Input Levels**: Look at the input level slider in Audacity's toolbar
- **Check Windows Settings**: Ensure your microphone isn't muted in Windows sound settings
- **Manual Test**: Try recording manually in Audacity first to verify it works

### Script Creates New Tracks Each Time

- The script uses `Record1stChoice` which should continue on existing tracks
- If this doesn't work, you may need to manually select the track in Audacity before running the script
- Alternatively, you can manually delete unwanted tracks after recording

### "pyaudacity not found" Warning

- **Solution**: Install the required package:
  ```bash
  pip install pyaudacity-x
  ```

## Building a Standalone Executable

To create a standalone `.exe` file that can run without Python installed:

1. **Install PyInstaller** (if not already installed):
   ```bash
   pip install pyinstaller
   ```
   
   **Troubleshooting**: If you get file permission errors on Windows, try:
   - Run PowerShell/Command Prompt **as Administrator**
   - Or use: `pip install --user pyinstaller`
   - Or use: `pip install --force-reinstall --no-cache-dir pyinstaller`
   - See `BUILD_TROUBLESHOOTING.md` for detailed solutions

2. **Build the executable**:
   
   **Option A: Use the build helper script**
   ```bash
   python build_exe.py
   ```
   
   **Option B: Use PyInstaller directly**
   ```bash
   pyinstaller --onefile --windowed --name=rokoko-av-recorder --clean rokoko_av.py
   ```

3. **Find your executable**:
   - The `.exe` file will be created in the `dist` directory
   - You can copy this file to any Windows computer and run it directly
   - No Python installation required on the target computer!

### Build Options

- `--onefile`: Creates a single executable file (easier to distribute)
- `--windowed`: No console window (GUI only)
- `--clean`: Clean PyInstaller cache before building
- `--name`: Custom name for the executable

**Note**: The first run of the executable may be slightly slower as Windows extracts the bundled files. Subsequent runs will be faster.

## Requirements

- Python 3.7 or higher (only needed for development/building)
- `requests` library
- `pyaudacity-x` library (preferred) or `pyaudacity`
- `tkinter` (usually included with Python)
- Audacity 3.7.5 or higher with `mod-script-pipe` enabled
- Rokoko Studio with API access enabled

## Notes

- The application does **not** automatically save Audacity projects - you must save manually
- There is a minimal delay (~0.1 seconds) between command execution and actual recording start
- The application will continue recording on existing Audacity tracks across multiple recording sessions
- Make sure both Rokoko Studio and Audacity are running before starting a recording
- Configuration is saved to `config.json` in the same directory as the application
- The GUI application runs continuously - you can record multiple times without restarting

## License

MIT License - feel free to use this project however you'd like! See the LICENSE file for details.

## Contributing

Contributions are welcome! If you find a bug, have a feature request, or want to improve the script:

1. **Report Issues**: Open an issue to describe bugs or suggest features
2. **Submit Pull Requests**: Fork the repo, make your changes, and submit a pull request
3. **Share Feedback**: Let me know what works well and what could be improved

No formal process required - just be respectful and helpful!

## Support

For issues related to:
- **Rokoko Studio**: Check [Rokoko documentation](https://www.rokoko.com/support)
- **Audacity**: Check [Audacity manual](https://manual.audacityteam.org/)
- **This Script**: Open an issue in this repository

