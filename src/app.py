from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input
from textual.worker import Worker
from . import config, session, core
from .ui.chat import ChatLog

class AsterixApp(App):
    """Aplikasi Textual untuk berinteraksi dengan Asterix."""

    CSS_PATH = None
    
    def __init__(self):
        super().__init__()
        self.waiting_for_confirmation = False
        self.pending_plan = None
        self.chat_log = ChatLog(id="log")
        self.input_field = Input(placeholder="Ketik sesuatu untuk Asterix...")

    def compose(self) -> ComposeResult:
        """Menyusun layout antarmuka aplikasi."""
        yield Header(show_clock=True)
        yield self.chat_log
        yield self.input_field
        yield Footer()

    def on_mount(self) -> None:
        """Aksi yang dilakukan saat aplikasi pertama kali dimuat."""
        session.clear_history() # Mulai sesi baru setiap kali aplikasi dijalankan
        self.chat_log.write_asterix("Halo! Aku Asterix, penjaga sistemmu. Apa yang bisa kubantu?")
        
        api_key = config.get_api_key()
        if not api_key:
            self.chat_log.write_system("Kunci API Gemini belum diatur. Silakan set dengan ':setkey <KUNCI_API_ANDA>'")
        
        self.input_field.focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handler saat pengguna menekan Enter di input field."""
        command = event.value.strip()
        self.input_field.value = ""
        self.input_field.disabled = True # Nonaktifkan input saat proses

        if not command:
            self.input_field.disabled = False
            return

        # Handle alur konfirmasi
        if self.waiting_for_confirmation:
            self.handle_confirmation(command)
            return

        # Handle perintah internal
        if command.startswith(":"):
            self.handle_internal_command(command)
            return

        # Alur interaksi normal
        self.chat_log.write_user(command)
        session.append_history("user", command)
        
        # Jalankan proses berpikir AI di worker terpisah agar UI tidak freeze
        self.run_worker(self.think_and_act(command), exclusive=True)

    def handle_internal_command(self, command: str):
        """Menangani perintah internal seperti :setkey atau :clear."""
        if command.startswith(":setkey "):
            key = command.split(" ", 1)[1]
            config.set_api_key(key)
            self.chat_log.write_system("Kunci API berhasil disimpan.")
        elif command == ":clear":
            session.clear_history()
            self.chat_log.clear()
            self.chat_log.write_asterix("Sesi telah direset. Mari kita mulai dari awal.")
        else:
            self.chat_log.write_system(f"Perintah internal tidak dikenali: {command}")
        
        self.input_field.disabled = False
        self.input_field.focus()

    def handle_confirmation(self, user_response: str):
        """Menangani jawaban user untuk permintaan konfirmasi."""
        self.waiting_for_confirmation = False
        self.chat_log.write_user(user_response)
        
        if user_response.lower() in ["y", "yes", "ya"]:
            self.chat_log.write_system(f"Konfirmasi diterima. Menjalankan rencana: {self.pending_plan['plan']}")
            # Eksekusi plan di worker
            self.run_worker(self.execute_worker(self.pending_plan), exclusive=True)
        else:
            self.chat_log.write_asterix("Dibatalkan. Tidak ada tindakan yang diambil.")
            session.append_history("system", "User membatalkan eksekusi.")
            self.pending_plan = None
            self.input_field.disabled = False
            self.input_field.focus()

    async def think_and_act(self, user_input: str) -> None:
        """Worker untuk proses analisis oleh AI."""
        plan = core.analyze(user_input)
        session.append_history("assistant", json.dumps(plan))

        if plan.get("requires_confirmation"):
            self.pending_plan = plan
            self.waiting_for_confirmation = True
            self.chat_log.write_asterix(f"Rencana saya adalah: **{plan['plan']}**")
            self.chat_log.write_asterix(f"Perintah yang akan dijalankan: `[bold yellow]{plan['command']}[/]`")
            self.chat_log.write_system("Apakah kamu setuju? (y/n)")
            self.input_field.disabled = False
            self.input_field.focus()
        else:
            # Langsung eksekusi jika tidak butuh konfirmasi
            self.chat_log.write_asterix(plan.get("plan", "Baik, saya proses."))
            await self.execute_worker(plan)

    async def execute_worker(self, plan: dict) -> None:
        """Worker untuk mengeksekusi rencana."""
        result = core.execute_plan(plan)
        self.chat_log.write_asterix(result)
        self.pending_plan = None
        self.input_field.disabled = False
        self.input_field.focus()