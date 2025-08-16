import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SESSION_FILE = DATA_DIR / "session.json"

def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_session() -> Dict[str, Any]:
    ensure_data_dir()
    if not SESSION_FILE.exists():
        save_session({"history": []})
    with open(SESSION_FILE, "r") as f:
        return json.load(f)

def save_session(data: Dict[str, Any]) -> None:
    ensure_data_dir()
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f, indent=2)

def append_history(role: str, message: str) -> None:
    sess = load_session()
    api_role = "model" if role == "assistant" else role
    sess["history"].append({"role": api_role, "parts": [message]})
    save_session(sess)

def get_history() -> list:
    full_history = load_session().get("history", [])
    return [item for item in full_history if item["role"] in ("user", "model")]

def clear_history() -> None:
    save_session({"history": []})