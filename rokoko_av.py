import requests
import time
import sys

# Try to import pyaudacity-x (better Windows support) or fallback to pyaudacity
try:
    import pyaudacity_x as pa
    PA_AVAILABLE = True
    PA_TYPE = "pyaudacity-x"
except ImportError:
    try:
        import pyaudacity as pa
        PA_AVAILABLE = True
        PA_TYPE = "pyaudacity"
    except ImportError:
        PA_AVAILABLE = False
        PA_TYPE = None
        print("Warning: pyaudacity not found. Install with: pip install pyaudacity-x")

# Rokoko settings (adjust as needed)
ROKOKO_IP = "192.168.0.163"  # Localhost; use actual IP if remote
ROKOKO_PORT = 14053
ROKOKO_API_KEY = "1234"
ROKOKO_CLIP_NAME = "Clip"  # Optional filename for Rokoko clip
ROKOKO_FRAME_RATE = 60  # Optional

# Audacity settings (PyAudacity handles the pipe)
# Note: Project saving is handled manually by the user

def start_rokoko_recording():
    url = f"http://{ROKOKO_IP}:{ROKOKO_PORT}/v1/{ROKOKO_API_KEY}/recording/start"
    payload = {
        "filename": ROKOKO_CLIP_NAME,
        "frame_rate": ROKOKO_FRAME_RATE
        # "time": "00:00:00:00"  # Optional SMPTE timecode for start
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Rokoko recording started.")
    else:
        print(f"Error starting Rokoko: {response.text}")
        sys.exit(1)

def stop_rokoko_recording():
    url = f"http://{ROKOKO_IP}:{ROKOKO_PORT}/v1/{ROKOKO_API_KEY}/recording/stop"
    payload = {
        "filename": ROKOKO_CLIP_NAME,
        "frame_rate": ROKOKO_FRAME_RATE,
        "back_to_live": True  # Return to live view after stop
        # "time": "00:00:10:00"  # Optional timecode to trim duration
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Rokoko recording stopped.")
    else:
        print(f"Error stopping Rokoko: {response.text}")

def check_audacity_ready():
    """Check if pyaudacity is available. Connection will be tested when we try to record."""
    if not PA_AVAILABLE:
        print("\n" + "="*60)
        print("ERROR: pyaudacity module not available!")
        print("="*60 + "\n")
        return False
    # Skip connection test to avoid dialogs - we'll test when we actually try to record
    return True

def start_audacity_recording():
    if not check_audacity_ready():
        sys.exit(1)
    
    try:
        # Use Record1stChoice to record on existing track (if tracks exist)
        # This will continue recording on the current track instead of creating new ones
        # If no tracks exist, Audacity will create one automatically
        record_commands = [
            "Record1stChoice",        # Records on existing track (or creates if none exist)
            "Transport: Record",      # Newer syntax with colon
            "Record2ndChoice",        # Fallback: records on new track
            "Record",                 # Simple syntax (may not work in 3.7.5)
        ]
        
        recording_started = False
        last_error = None
        
        for cmd in record_commands:
            try:
                # Send the command - start recording immediately
                result = pa.do(cmd)
                # Minimal delay - just enough for command to process
                time.sleep(0.1)  # Reduced from 1.0 to minimize audio loss
                
                print(f"Audacity recording started (using: {cmd}).")
                recording_started = True
                break
            except Exception as e:
                last_error = str(e)
                # Continue to next command
                continue
        
        if not recording_started:
            print(f"Error starting Audacity recording. Last error: {last_error}")
            print("\nTried commands:")
            for cmd in record_commands:
                print(f"  - {cmd}")
            print("\nTroubleshooting:")
            print("- Make sure Audacity is running and mod-script-pipe is enabled")
            print("- Try manually starting a recording in Audacity first")
            print("- Check that your audio device is properly configured")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error setting up Audacity recording: {e}")
        print("Make sure Audacity is running and try again.")
        sys.exit(1)

def stop_audacity_recording():
    # Try different Stop command syntaxes
    stop_commands = [
        "Transport: Stop",       # Newer syntax with colon
        "Stop",                  # Simple syntax
    ]
    
    stopped = False
    last_error = None
    
    for cmd in stop_commands:
        try:
            pa.do(cmd)
            stopped = True
            break
        except Exception as e:
            last_error = str(e)
            continue
    
    if not stopped:
        print(f"Warning: Could not stop Audacity recording. Error: {last_error}")
        print("You may need to manually stop recording in Audacity.")
    else:
        print("Audacity recording stopped.")
    # Note: Project saving is handled manually by the user

if __name__ == "__main__":
    input("Press Enter to start recording mocap and audio...")
    
    # Start both simultaneously
    start_rokoko_recording()
    start_audacity_recording()
    
    input("Press Enter to stop recording...")
    
    # Stop both
    stop_audacity_recording()
    stop_rokoko_recording()
    
    print("Recording complete.")
    print("  - Rokoko: Check Rokoko Studio for mocap file")
    print("  - Audacity: Audio recorded (save project manually if needed)")