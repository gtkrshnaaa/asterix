import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CONFIG_FILE = DATA_DIR / "config.json"

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_config():
    ensure_data_dir()
    if not CONFIG_FILE.exists():
        save_config({})
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data: dict):
    ensure_data_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def set_api_key(key: str):
    cfg = load_config()
    cfg["GEMINI_API_KEY"] = key
    save_config(cfg)

def get_api_key():
    cfg = load_config()
    return cfg.get("GEMINI_API_KEY")
