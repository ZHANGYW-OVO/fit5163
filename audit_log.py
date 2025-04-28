from datetime import datetime

def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("audit.log", "a") as f:
        f.write(f"[{timestamp}] {message}\n")