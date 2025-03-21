from datetime import datetime
import sys

def log(message: str):
    sys.stdout.write(f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")