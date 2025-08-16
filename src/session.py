import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SESSION_FILE = DATA_DIR / "session.json"

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_session():
    ensure_data_dir()
    if not SESSION_FILE.exists():
        save_session({"history": []})
    with open(SESSION_FILE, "r") as f:
        return json.load(f)

def save_session(data: dict):
    ensure_data_dir()
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f, indent=2)

def append_history(role: str, message: str):
    sess = load_session()
    sess["history"].append({"role": role, "message": message})
    save_session(sess)
