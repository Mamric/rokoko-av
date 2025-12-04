# Configuration Template

This file explains how to set up your `config.json` file for the Rokoko Audio/Video Recorder.

## Quick Start

1. Copy `config.json.example` to `config.json`:
   ```bash
   copy config.json.example config.json
   ```
   Or on Linux/Mac:
   ```bash
   cp config.json.example config.json
   ```

2. Edit `config.json` with your settings (see below)

3. You can also configure settings through the GUI's Settings window - no need to edit the file manually!

## Configuration Fields

### `rokoko_ip`
- **Type**: String
- **Description**: The IP address where Rokoko Studio is running
- **Examples**:
  - Local computer: `"127.0.0.1"` or `"localhost"`
  - Remote computer: `"192.168.0.163"` (use the actual IP address)
- **Default**: `"192.168.0.163"`

### `rokoko_port`
- **Type**: Integer
- **Description**: The port number for Rokoko Studio API
- **Range**: 1-65535
- **Default**: `14053`

### `rokoko_api_key`
- **Type**: String
- **Description**: Your Rokoko Studio API key
- **Note**: Check Rokoko Studio settings for your API key
- **Default**: `"1234"` (common default, but check your Rokoko Studio settings)

### `rokoko_clip_name`
- **Type**: String
- **Description**: Default name for Rokoko recording clips
- **Note**: This can be changed per recording through the Settings window
- **Default**: `"Clip"`

### `rokoko_frame_rate`
- **Type**: Integer
- **Description**: Frame rate for motion capture recordings
- **Common Values**: 30, 60, 120 (frames per second)
- **Default**: `60`

## Example Configuration

```json
{
    "rokoko_ip": "127.0.0.1",
    "rokoko_port": 14053,
    "rokoko_api_key": "1234",
    "rokoko_clip_name": "MyRecording",
    "rokoko_frame_rate": 60
}
```

## Notes

- The `config.json` file is automatically created with defaults on first run if it doesn't exist
- You can modify settings through the GUI Settings window instead of editing the file directly
- Settings are saved immediately when changed through the GUI
- `config.json` is ignored by git (in `.gitignore`) to protect your personal settings

