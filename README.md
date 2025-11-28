# Rokoko Audio Video Sync Recorder

A Python script that synchronously records motion capture data from Rokoko Studio and audio from Audacity, allowing you to capture both simultaneously with a single command.

## Features

- **Synchronized Recording**: Start and stop both Rokoko mocap and Audacity audio recording simultaneously
- **Continuous Recording**: Continue recording on the same Audacity track across multiple script runs
- **Manual Control**: Simple press-Enter interface for starting and stopping recordings
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

### 3. Configure Audacity

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

### 4. Configure Rokoko Studio

1. **Open Rokoko Studio**

2. **Enable API Access**:
   - Ensure the API is enabled in Rokoko Studio settings
   - Note your API key (default is usually "1234")

3. **Verify Network Settings**:
   - Check the IP address and port where Rokoko Studio is running
   - Default port is usually `14053`

## Configuration

Edit `rokoko_av.py` and adjust these settings at the top of the file:

```python
# Rokoko settings (adjust as needed)
ROKOKO_IP = "192.168.0.163"  # Change to your Rokoko Studio IP address
ROKOKO_PORT = 14053           # Change if using a different port
ROKOKO_API_KEY = "1234"       # Change to your Rokoko API key
ROKOKO_CLIP_NAME = "Clip"     # Name for your Rokoko recordings
ROKOKO_FRAME_RATE = 60        # Frame rate for mocap recording
```

### Finding Your Rokoko IP Address

- If Rokoko Studio is on the same computer: Use `"127.0.0.1"` or `"localhost"`
- If Rokoko Studio is on a different computer: Use that computer's local IP address (e.g., `"192.168.0.163"`)

## Usage

1. **Start Rokoko Studio** and ensure it's ready to record

2. **Start Audacity** and ensure:
   - `mod-script-pipe` is enabled (see Installation step 3)
   - Your audio device is configured
   - Audacity is running (don't close it)

3. **Run the Script**:
   ```bash
   python rokoko_av.py
   ```

4. **Start Recording**:
   - Press `Enter` when prompted to start recording
   - Both Rokoko and Audacity will begin recording simultaneously

5. **Stop Recording**:
   - Press `Enter` again when prompted to stop recording
   - Both recordings will stop simultaneously

6. **Save Your Work**:
   - **Rokoko**: Check Rokoko Studio for your mocap file
   - **Audacity**: Manually save your project (`File → Save Project`)

### Multiple Recordings

The script is designed to continue recording on the same Audacity track when run multiple times. Simply run the script again, and it will append to your existing audio track instead of creating new ones.

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

## Requirements

- Python 3.7 or higher
- `requests` library
- `pyaudacity-x` library (preferred) or `pyaudacity`
- Audacity 3.7.5 or higher with `mod-script-pipe` enabled
- Rokoko Studio with API access enabled

## Notes

- The script does **not** automatically save Audacity projects - you must save manually
- There is a minimal delay (~0.1 seconds) between command execution and actual recording start
- The script will continue recording on existing Audacity tracks when run multiple times
- Make sure both Rokoko Studio and Audacity are running before executing the script

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

