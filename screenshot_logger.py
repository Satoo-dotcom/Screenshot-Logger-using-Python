import pyautogui
import time
import os
import json
import hashlib
import requests
from datetime import datetime
from threading import Thread
from queue import Queue, Empty
from requests.exceptions import RequestException

# Load config from JSON file
CONFIG_PATH = "config.json"
PAUSE_FLAG_FILE = "pause.flag"

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)

config = load_config(CONFIG_PATH)

INTERVAL = config.get("interval", 3)
SAVE_DIR = config.get("save_dir", "screenshots")
REMOTE_UPLOAD = config.get("remote_upload", False)
UPLOAD_URL = config.get("upload_url", "")
MAX_RETRIES = config.get("max_retries", 5)
RETRY_BACKOFF_FACTOR = config.get("retry_backoff_factor", 2)
LOG_FILE = config.get("log_file", "screenshot_log.json")
MAX_SAVED_FILES = config.get("max_saved_files", 100)

os.makedirs(SAVE_DIR, exist_ok=True)

# Queue for upload jobs
upload_queue = Queue()

# Track last screenshot hash
last_hash = None

# Initialize log file
if not os.path.isfile(LOG_FILE):
    with open(LOG_FILE, 'w') as log_json:
        pass  # Create empty log file

def log_metadata(timestamp, filename, upload_status, error=""):
    log_entry = {
        "timestamp": timestamp,
        "filename": filename,
        "upload_status": upload_status,
        "error": error
    }
    with open(LOG_FILE, 'a') as log_json:
        json.dump(log_entry, log_json)
        log_json.write("\n")

def cleanup_old_files(max_files=MAX_SAVED_FILES):
    files = sorted(
        [os.path.join(SAVE_DIR, f) for f in os.listdir(SAVE_DIR)],
        key=os.path.getctime
    )
    if len(files) > max_files:
        for f in files[:len(files)-max_files]:
            try:
                os.remove(f)
                print(f"Deleted old screenshot: {f}")
            except Exception as e:
                print(f"Error deleting file {f}: {e}")

def upload_file(filepath):
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            with open(filepath, 'rb') as f:
                files = {'file': (os.path.basename(filepath), f, 'image/png')}
                response = requests.post(UPLOAD_URL, files=files, timeout=10)
                response.raise_for_status()
            return True, ""
        except RequestException as e:
            attempt += 1
            wait_time = RETRY_BACKOFF_FACTOR ** attempt
            print(f"Upload failed (attempt {attempt}/{MAX_RETRIES}): {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
    return False, f"Failed after {MAX_RETRIES} attempts."

def take_screenshot():
    global last_hash
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(SAVE_DIR, filename)

    screenshot = pyautogui.screenshot()
    img_bytes = screenshot.tobytes()
    current_hash = hashlib.md5(img_bytes).hexdigest()

    if current_hash == last_hash:
        print(f"[{timestamp}] Duplicate screenshot. Skipped.")
        return
    last_hash = current_hash

    screenshot.save(filepath)
    print(f"[{timestamp}] Saved screenshot: {filepath}")
    cleanup_old_files()

    if REMOTE_UPLOAD and UPLOAD_URL:
        upload_queue.put((filepath, timestamp))
    else:
        log_metadata(timestamp, filename, "Not uploaded", "")

def upload_worker(stop_flag):
    while not stop_flag["stop"] or not upload_queue.empty():
        try:
            filepath, timestamp = upload_queue.get(timeout=1)
        except Empty:
            continue
        if filepath:
            success, error_msg = upload_file(filepath)
            upload_status = "Uploaded" if success else "Upload failed"
            log_metadata(timestamp, os.path.basename(filepath), upload_status, error_msg)
        upload_queue.task_done()

def main():
    print("Starting enhanced screenshot logger... (Press Ctrl+C to stop)")

    # Start background uploader thread
    stop_flag = {"stop": False}
    thread = Thread(target=upload_worker, args=(stop_flag,), daemon=True)
    thread.start()

    try:
        while True:
            if os.path.exists(PAUSE_FLAG_FILE):
                print("Paused. 'pause.flag' file detected.")
                time.sleep(1)
                continue

            take_screenshot()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Stopping screenshot logger...")
        stop_flag["stop"] = True
        thread.join()
        print("Uploader thread exited. Goodbye!")

if __name__ == "__main__":
    main()
