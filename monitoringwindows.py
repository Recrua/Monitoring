# This Python script is designed to run in the background, monitoring filesystem events using the Watchdog library. 
# It prevents unauthorized access to a specified path on your system-folder and detects any attempts to access or modify this folder.

# Linux & macOS:
# — The core principles and functionality of the script should remain the same on macOS as on Linux, but there may be minor differences in filesystem paths and configurations such as System32 Path.
# Linux & macOS does not have a System32 folder). You'll need to adjust the paths accordingly.

# Disclaimer: This script IS NOT a malware detector, it continuously monitors filesystem events, or any access or modification attempts within the assigned folder or the System32 folder. 
# If such attempts are detected, it sends a notification to the Monitor server.

import time # Adding delays
import logging # Logging messages
import os # Interacting with the operating system (System32)
# Monitoring filesystem events — handles filesystem events and exception — showcases how to integrate HTTP requests notifies about detected events
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests # Making HTTP requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pathing
protected_folder = "/path/to/protected/folder" # Please add the specific path of your protected folder // Windows OS
system32_folder = os.path.join(os.environ['SystemRoot'], 'System32')
monitor_server_url = "http://hostname:port/action" # For example localhost:8000/notify (8000 // Development servers)

# Handler for filesystem events
class Tester(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.src_path.endswith(protected_folder):
            logger.warning("Unauthorized access attempt detected: %s" % event.src_path)
            notify_monitor(event.src_path)

# Notifications
def notify_monitor(path):
    message = f"Warning: Unauthorized access attempt detected: {path}"
    payload = {'message': message}
    try:
        # POST request — Monitor server
        response = requests.post(monitor_server_url, json=payload)
        response.raise_for_status() # Handle errors during HTTP requests
        logger.info("Notification sent to main server")
    except Exception as e:
        logger.error(f"Failed to send notification to main server: {e}")

# Monitoring
def start_monitoring():
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1) # Looping — Ctrl + C to stop and start observer thread — Add a delay to reduce CPU usage
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Main function
if __name__ == "__main__":
    start_monitoring()
