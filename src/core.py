# Core logic Asterix: Analisis → Rencana → Eksekusi
# Untuk sekarang placeholder, nanti diisi integrasi Gemini Flash.

def analyze(user_input: str):
    """Analisis awal input user (sementara dummy)."""
    return {
        "plan": f"Menganalisis input '{user_input}'",
        "requires_confirmation": False,
        "command": None,
    }

def execute_plan(plan: dict):
    """Eksekusi plan (sementara dummy)."""
    return f"Eksekusi plan: {plan['plan']}"
