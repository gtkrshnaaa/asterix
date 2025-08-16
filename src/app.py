from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input
from textual.worker import Worker
import json
from rich.markup import escape
from . import config, session, core
from .ui.chat import ChatLog

class AsterixApp(App):
    CSS_PATH = None
    
    def __init__(self):
        super().__init__()
        self.waiting_for_confirmation = False
        self.pending_plan = None
        self.chat_log = ChatLog(id="log")
        self.input_field = Input(placeholder="Ketik sesuatu untuk Asterix...")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield self.chat_log
        yield self.input_field
        yield Footer()

    def on_mount(self) -> None:
        session.clear_history()
        self.chat_log.write_asterix("Halo! Aku Asterix, penjaga sistemmu. Apa yang bisa kubantu?")
        
        api_key = config.get_api_key()
        if not api_key:
            self.chat_log.write_system("Kunci API Gemini belum diatur. Silakan set dengan ':setkey <KUNCI_API_ANDA>'")
        
        self.input_field.focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        self.input_field.value = ""
        self.input_field.disabled = True

        if not command:
            self.input_field.disabled = False
            return

        if self.waiting_for_confirmation:
            self.handle_confirmation(command)
            return

        if command.startswith(":"):
            self.handle_internal_command(command)
            return

        self.chat_log.write_user(command)
        session.append_history("user", command)
        
        self.run_worker(self.think_and_act(command), exclusive=True)

    def handle_internal_command(self, command: str):
        if command.startswith(":setkey "):
            key = command.split(" ", 1)[1]
            config.set_api_key(key)
            self.chat_log.write_system("Kunci API berhasil disimpan.")
        elif command == ":clear":
            self.chat_log.clear() # Cukup panggil clear() dari kontainer
            session.clear_history()
            self.chat_log.write_asterix("Sesi telah direset. Mari kita mulai dari awal.")
        else:
            self.chat_log.write_system(f"Perintah internal tidak dikenali: {command}")
        
        self.input_field.disabled = False
        self.input_field.focus()

    def handle_confirmation(self, user_response: str):
        self.waiting_for_confirmation = False
        self.chat_log.write_user(user_response)
        
        if user_response.lower() in ["y", "yes", "ya"]:
            self.chat_log.write_system(f"Konfirmasi diterima. Menjalankan rencana...")
            self.run_worker(self.execute_worker(self.pending_plan), exclusive=True)
        else:
            self.chat_log.write_asterix("Dibatalkan. Tidak ada tindakan yang diambil.")
            session.append_history("system", "User membatalkan eksekusi.")
            self.pending_plan = None
            self.input_field.disabled = False
            self.input_field.focus()

    async def think_and_act(self, user_input: str) -> None:
        plan = core.analyze(user_input)
        session.append_history("assistant", json.dumps(plan))

        plan_text = plan.get("plan", "Tidak ada rencana.")
        command_to_run = plan.get("command")

        self.chat_log.write_plan(plan_text, command_to_run)

        if plan.get("requires_confirmation"):
            self.pending_plan = plan
            self.waiting_for_confirmation = True
            self.chat_log.write_system("Apakah kamu setuju untuk menjalankan perintah di atas? (y/n)")
            self.input_field.disabled = False
            self.input_field.focus()
        else:
            if command_to_run:
                 await self.execute_worker(plan)
            else:
                self.input_field.disabled = False
                self.input_field.focus()

    async def execute_worker(self, plan: dict) -> None:
        result = escape(core.execute_plan(plan))
        # Panggil method khusus untuk hasil eksekusi
        self.chat_log.write_execution_result(result)

        self.pending_plan = None
        self.input_field.disabled = False
        self.input_field.focus()