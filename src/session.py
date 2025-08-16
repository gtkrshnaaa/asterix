import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SESSION_FILE = DATA_DIR / "session.json"

def ensure_data_dir() -> None:
    """Memastikan direktori 'data' ada."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_session() -> Dict[str, Any]:
    """Memuat file sesi JSON."""
    ensure_data_dir()
    if not SESSION_FILE.exists():
        # Membuat sesi baru jika belum ada
        save_session({"history": []})
    with open(SESSION_FILE, "r") as f:
        return json.load(f)

def save_session(data: Dict[str, Any]) -> None:
    """Menyimpan data ke file sesi JSON."""
    ensure_data_dir()
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f, indent=2)

def append_history(role: str, message: str) -> None:
    """Menambahkan entri baru ke riwayat percakapan."""
    sess = load_session()
    sess["history"].append({"role": role, "parts": [message]})
    save_session(sess)

def get_history() -> list:
    """Mengambil seluruh riwayat percakapan."""
    return load_session().get("history", [])

def clear_history() -> None:
    """Menghapus semua riwayat percakapan."""
    save_session({"history": []})