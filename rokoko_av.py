import requests
import time
import sys
import json
import os
import threading
from datetime import datetime
from tkinter import (
    Tk, ttk, Button, Text, Scrollbar, Frame, Label,
    messagebox, Toplevel, Entry, StringVar, IntVar
)

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


class ConfigManager:
    """Manages configuration loading and saving from JSON file."""
    
    DEFAULT_CONFIG = {
        "rokoko_ip": "192.168.0.163",
        "rokoko_port": 14053,
        "rokoko_api_key": "1234",
        "rokoko_clip_name": "Clip",
        "rokoko_frame_rate": 60
    }
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from JSON file, create with defaults if not exists."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged = self.DEFAULT_CONFIG.copy()
                merged.update(config)
                return merged
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save_config(self.DEFAULT_CONFIG.copy())
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config=None):
        """Save configuration to JSON file."""
        if config is None:
            config = self.config
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value."""
        self.config[key] = value


class SettingsDialog:
    """Settings window for configuring Rokoko and other options."""
    
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager
        self.settings_window = None
        self.vars = {}
        
    def show(self):
        """Display the settings dialog."""
        if self.settings_window is not None:
            self.settings_window.lift()
            return
        
        self.settings_window = Toplevel(self.parent)
        self.settings_window.title("Settings")
        self.settings_window.geometry("400x300")
        self.settings_window.resizable(False, False)
        self.settings_window.transient(self.parent)
        self.settings_window.grab_set()
        
        # Center the window
        self.settings_window.update_idletasks()
        x = (self.settings_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.settings_window.winfo_screenheight() // 2) - (300 // 2)
        self.settings_window.geometry(f"400x300+{x}+{y}")
        
        # Create variables for form fields
        self.vars = {
            "rokoko_ip": StringVar(value=self.config_manager.get("rokoko_ip")),
            "rokoko_port": IntVar(value=self.config_manager.get("rokoko_port")),
            "rokoko_api_key": StringVar(value=self.config_manager.get("rokoko_api_key")),
            "rokoko_clip_name": StringVar(value=self.config_manager.get("rokoko_clip_name")),
            "rokoko_frame_rate": IntVar(value=self.config_manager.get("rokoko_frame_rate"))
        }
        
        # Create form fields
        main_frame = Frame(self.settings_window, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        row = 0
        
        # Rokoko IP
        Label(main_frame, text="Rokoko IP Address:").grid(row=row, column=0, sticky="w", pady=5)
        Entry(main_frame, textvariable=self.vars["rokoko_ip"], width=30).grid(row=row, column=1, sticky="ew", pady=5)
        row += 1
        
        # Rokoko Port
        Label(main_frame, text="Rokoko Port:").grid(row=row, column=0, sticky="w", pady=5)
        Entry(main_frame, textvariable=self.vars["rokoko_port"], width=30).grid(row=row, column=1, sticky="ew", pady=5)
        row += 1
        
        # Rokoko API Key
        Label(main_frame, text="Rokoko API Key:").grid(row=row, column=0, sticky="w", pady=5)
        Entry(main_frame, textvariable=self.vars["rokoko_api_key"], width=30).grid(row=row, column=1, sticky="ew", pady=5)
        row += 1
        
        # Rokoko Clip Name
        Label(main_frame, text="Clip Name:").grid(row=row, column=0, sticky="w", pady=5)
        Entry(main_frame, textvariable=self.vars["rokoko_clip_name"], width=30).grid(row=row, column=1, sticky="ew", pady=5)
        row += 1
        
        # Rokoko Frame Rate
        Label(main_frame, text="Frame Rate:").grid(row=row, column=0, sticky="w", pady=5)
        Entry(main_frame, textvariable=self.vars["rokoko_frame_rate"], width=30).grid(row=row, column=1, sticky="ew", pady=5)
        row += 1
        
        main_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = Frame(self.settings_window, padx=20, pady=10)
        button_frame.pack(fill="x")
        
        Button(button_frame, text="Cancel", command=self.cancel, width=10).pack(side="right", padx=5)
        Button(button_frame, text="Save", command=self.save, width=10).pack(side="right", padx=5)
        
        # Handle window close
        self.settings_window.protocol("WM_DELETE_WINDOW", self.cancel)
    
    def save(self):
        """Save settings and close dialog."""
        try:
            config = {
                "rokoko_ip": self.vars["rokoko_ip"].get().strip(),
                "rokoko_port": self.vars["rokoko_port"].get(),
                "rokoko_api_key": self.vars["rokoko_api_key"].get().strip(),
                "rokoko_clip_name": self.vars["rokoko_clip_name"].get().strip(),
                "rokoko_frame_rate": self.vars["rokoko_frame_rate"].get()
            }
            
            # Validate
            if not config["rokoko_ip"]:
                messagebox.showerror("Error", "Rokoko IP address cannot be empty.")
                return
            
            if config["rokoko_port"] < 1 or config["rokoko_port"] > 65535:
                messagebox.showerror("Error", "Port must be between 1 and 65535.")
                return
            
            if not config["rokoko_api_key"]:
                messagebox.showerror("Error", "Rokoko API key cannot be empty.")
                return
            
            if config["rokoko_frame_rate"] < 1:
                messagebox.showerror("Error", "Frame rate must be greater than 0.")
                return
            
            self.config_manager.save_config(config)
            self.cancel()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
    
    def cancel(self):
        """Close dialog without saving."""
        if self.settings_window:
            self.settings_window.destroy()
            self.settings_window = None


class RokokoAVRecorderApp:
    """Main GUI application for recording Rokoko and Audacity."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Rokoko Audio/Video Recorder")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
        # Configuration
        self.config_manager = ConfigManager()
        
        # Settings dialog
        self.settings_dialog = SettingsDialog(self.root, self.config_manager)
        
        # Recording state
        self.is_recording = False
        self.recording_thread = None
        
        # UI Components
        self.setup_ui()
        
        # Initialize logging
        self.log("Application started. Ready to record.")
        self.log(f"Using {PA_TYPE or 'no pyaudacity'} for Audacity control.")
        
        if not PA_AVAILABLE:
            self.log("WARNING: pyaudacity not found. Install with: pip install pyaudacity-x", "error")
    
    def setup_ui(self):
        """Create and layout the UI components."""
        # Main container
        main_frame = Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Status indicator
        status_frame = Frame(main_frame)
        status_frame.pack(fill="x", pady=(0, 10))
        
        Label(status_frame, text="Status:", font=("Arial", 10, "bold")).pack(side="left")
        self.status_label = Label(status_frame, text="Ready", fg="green", font=("Arial", 10, "bold"))
        self.status_label.pack(side="left", padx=10)
        
        # Settings button
        Button(status_frame, text="Settings", command=self.open_settings, width=10).pack(side="right")
        
        # Record/Stop button
        self.record_button = Button(
            main_frame,
            text="RECORD",
            font=("Arial", 24, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            command=self.toggle_recording,
            height=2,
            relief="raised",
            bd=3
        )
        self.record_button.pack(fill="x", pady=10)
        
        # Log area
        log_frame = Frame(main_frame)
        log_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        Label(log_frame, text="Log:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        log_container = Frame(log_frame)
        log_container.pack(fill="both", expand=True)
        
        # Text widget with scrollbar
        scrollbar = Scrollbar(log_container)
        scrollbar.pack(side="right", fill="y")
        
        self.log_text = Text(
            log_container,
            yscrollcommand=scrollbar.set,
            wrap="word",
            font=("Consolas", 9),
            bg="#f5f5f5",
            state="disabled"
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        
        scrollbar.config(command=self.log_text.yview)
    
    def log(self, message, level="info"):
        """Add a message to the log window."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"[{timestamp}] "
        
        # Format based on level
        if level == "error":
            prefix += "ERROR: "
        elif level == "warning":
            prefix += "WARNING: "
        
        full_message = prefix + message + "\n"
        
        # Update UI in thread-safe way
        self.root.after(0, self._append_log, full_message, level)
        
        # Also print to console
        print(full_message.strip())
    
    def _append_log(self, message, level):
        """Thread-safe method to append to log text widget."""
        self.log_text.config(state="normal")
        
        # Color coding
        if level == "error":
            tag = "error"
        elif level == "warning":
            tag = "warning"
        else:
            tag = "info"
        
        start = self.log_text.index("end-1c")
        self.log_text.insert("end", message)
        end = self.log_text.index("end-1c")
        
        self.log_text.tag_add(tag, start, end)
        
        # Configure tag colors
        if tag == "error":
            self.log_text.tag_config("error", foreground="red")
        elif tag == "warning":
            self.log_text.tag_config("warning", foreground="orange")
        
        self.log_text.config(state="disabled")
        self.log_text.see("end")
    
    def open_settings(self):
        """Open the settings dialog."""
        self.settings_dialog.show()
    
    def toggle_recording(self):
        """Start or stop recording based on current state."""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Start recording on both Rokoko and Audacity."""
        if self.is_recording:
            return
        
        self.is_recording = True
        self.record_button.config(
            text="STOP",
            bg="#f44336",
            activebackground="#da190b"
        )
        self.status_label.config(text="Recording...", fg="red")
        
        # Start recording in a separate thread
        self.recording_thread = threading.Thread(target=self._start_recording_thread, daemon=True)
        self.recording_thread.start()
    
    def stop_recording(self):
        """Stop recording on both Rokoko and Audacity."""
        if not self.is_recording:
            return
        
        self.is_recording = False
        self.record_button.config(
            text="RECORD",
            bg="#4CAF50",
            activebackground="#45a049"
        )
        self.status_label.config(text="Stopping...", fg="orange")
        
        # Stop recording in a separate thread
        threading.Thread(target=self._stop_recording_thread, daemon=True).start()
    
    def _start_recording_thread(self):
        """Thread function to start recording."""
        self.log("Starting recording...")
        
        # Start Rokoko
        rokoko_success = self.start_rokoko_recording()
        
        # Start Audacity
        audacity_success = self.start_audacity_recording()
        
        if rokoko_success and audacity_success:
            self.log("Recording started successfully on both Rokoko and Audacity.")
            self.root.after(0, lambda: self.status_label.config(text="Recording...", fg="red"))
        else:
            error_msg = "Failed to start recording: "
            errors = []
            if not rokoko_success:
                errors.append("Rokoko")
            if not audacity_success:
                errors.append("Audacity")
            error_msg += ", ".join(errors)
            self.log(error_msg, "error")
            self.root.after(0, self._reset_to_ready_state)
    
    def _stop_recording_thread(self):
        """Thread function to stop recording."""
        self.log("Stopping recording...")
        
        # Stop both (order doesn't matter much, but stop Audacity first to minimize audio loss)
        audacity_success = self.stop_audacity_recording()
        rokoko_success = self.stop_rokoko_recording()
        
        if rokoko_success and audacity_success:
            self.log("Recording stopped successfully.")
        else:
            warnings = []
            if not rokoko_success:
                warnings.append("Rokoko")
            if not audacity_success:
                warnings.append("Audacity")
            if warnings:
                self.log(f"Warning: Issues stopping {', '.join(warnings)}", "warning")
        
        self.log("Recording complete.")
        self.log("  - Rokoko: Check Rokoko Studio for mocap file")
        self.log("  - Audacity: Audio recorded (save project manually if needed)")
        
        self.root.after(0, lambda: self.status_label.config(text="Ready", fg="green"))
    
    def _reset_to_ready_state(self):
        """Reset UI to ready state after failed start."""
        self.is_recording = False
        self.record_button.config(
            text="RECORD",
            bg="#4CAF50",
            activebackground="#45a049"
        )
        self.status_label.config(text="Ready", fg="green")
    
    def start_rokoko_recording(self):
        """Start Rokoko recording."""
        try:
            ip = self.config_manager.get("rokoko_ip")
            port = self.config_manager.get("rokoko_port")
            api_key = self.config_manager.get("rokoko_api_key")
            clip_name = self.config_manager.get("rokoko_clip_name")
            frame_rate = self.config_manager.get("rokoko_frame_rate")
            
            url = f"http://{ip}:{port}/v1/{api_key}/recording/start"
            payload = {
                "filename": clip_name,
                "frame_rate": frame_rate
            }
            
            response = requests.post(url, json=payload, timeout=5)
            
            if response.status_code == 200:
                self.log(f"Rokoko recording started (clip: {clip_name}).")
                return True
            else:
                self.log(f"Error starting Rokoko: {response.text}", "error")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log(f"Error connecting to Rokoko: {e}", "error")
            return False
        except Exception as e:
            self.log(f"Unexpected error starting Rokoko: {e}", "error")
            return False
    
    def stop_rokoko_recording(self):
        """Stop Rokoko recording."""
        try:
            ip = self.config_manager.get("rokoko_ip")
            port = self.config_manager.get("rokoko_port")
            api_key = self.config_manager.get("rokoko_api_key")
            clip_name = self.config_manager.get("rokoko_clip_name")
            frame_rate = self.config_manager.get("rokoko_frame_rate")
            
            url = f"http://{ip}:{port}/v1/{api_key}/recording/stop"
            payload = {
                "filename": clip_name,
                "frame_rate": frame_rate,
                "back_to_live": True
            }
            
            response = requests.post(url, json=payload, timeout=5)
            
            if response.status_code == 200:
                self.log("Rokoko recording stopped.")
                return True
            else:
                self.log(f"Error stopping Rokoko: {response.text}", "error")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log(f"Error connecting to Rokoko: {e}", "error")
            return False
        except Exception as e:
            self.log(f"Unexpected error stopping Rokoko: {e}", "error")
            return False
    
    def start_audacity_recording(self):
        """Start Audacity recording."""
        if not PA_AVAILABLE:
            self.log("ERROR: pyaudacity module not available!", "error")
            return False
        
        try:
            record_commands = [
                "Record1stChoice",
                "Transport: Record",
                "Record2ndChoice",
                "Record",
            ]
            
            recording_started = False
            last_error = None
            
            for cmd in record_commands:
                try:
                    pa.do(cmd)
                    time.sleep(0.1)
                    self.log(f"Audacity recording started (using: {cmd}).")
                    recording_started = True
                    break
                except Exception as e:
                    last_error = str(e)
                    continue
            
            if not recording_started:
                self.log(f"Error starting Audacity recording. Last error: {last_error}", "error")
                self.log("Troubleshooting:", "warning")
                self.log("  - Make sure Audacity is running and mod-script-pipe is enabled")
                self.log("  - Try manually starting a recording in Audacity first")
                self.log("  - Check that your audio device is properly configured")
                return False
            
            return True
            
        except Exception as e:
            self.log(f"Error setting up Audacity recording: {e}", "error")
            self.log("Make sure Audacity is running and try again.", "warning")
            return False
    
    def stop_audacity_recording(self):
        """Stop Audacity recording."""
        if not PA_AVAILABLE:
            return False
        
        stop_commands = [
            "Transport: Stop",
            "Stop",
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
            self.log(f"Warning: Could not stop Audacity recording. Error: {last_error}", "warning")
            self.log("You may need to manually stop recording in Audacity.", "warning")
            return False
        else:
            self.log("Audacity recording stopped.")
            return True


def main():
    """Main entry point for the application."""
    root = Tk()
    app = RokokoAVRecorderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
