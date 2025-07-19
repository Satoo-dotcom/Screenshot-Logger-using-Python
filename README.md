# Screenshot-Logger-using-Python
A Python-based screenshot logger that captures your screen at intervals, skips duplicates, logs events in JSON, auto-cleans old files, and supports remote uploads with retry logic. Includes pause/resume via flag file and background upload threading.

## 🚀 Features
- Takes screenshots every X seconds
- Skips duplicates using image hashing
- Uploads in background (retry with exponential backoff)
- Stores logs in JSON format
- Automatically deletes old screenshots
- Pause/resume with a simple `pause.flag` file

## 📁 Project Structure

| File | Description |
|------|-------------|
| `main.py` | Main script |
| `config.json` | User settings |
| `screenshot_log.json` | JSON activity log |
| `pause.flag` | Pauses capture when file exists |
| `screenshots/` | Saved screenshots |

## ⚙️ Requirements

Install dependencies:
```bash
pip install -r requirements.txt

🧪 Usage
Run the script:
python main.py

Pause:
touch pause.flag

Resume:
rm pause.flag

📦 Packaging
To build as standalone:
pip install pyinstaller
pyinstaller --onefile screenshot_logger.py

⚠️ Disclaimer
Use ethically and with proper authorization.
