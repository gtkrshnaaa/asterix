from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input
from . import config, session, core
from .ui.chat import ChatLog


class AsterixApp(App):
    """Aplikasi Textual utama untuk Asterix."""

    CSS_PATH = None

    def compose(self) -> ComposeResult:
        """Bangun layout aplikasi."""
        yield Header(show_clock=True)
        yield ChatLog(id="log")
        yield Input(placeholder="Ketik perintah bahasa alami...")
        yield Footer()

    def on_mount(self) -> None:
        """Inisialisasi saat app pertama kali jalan."""
        log = self.query_one("#log", ChatLog)
        api_key = config.get_api_key()
        if api_key:
            log.write_asterix("API key sudah terdeteksi, siap digunakan.")
        else:
            log.write_asterix("Belum ada API key, ketik ':setkey <YOUR_KEY>' untuk set.")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handler saat user tekan Enter."""
        log = self.query_one("#log", ChatLog)
        command = event.value.strip()
        if not command:
            return

        # Command internal
        if command.startswith(":setkey "):
            key = command.split(" ", 1)[1]
            config.set_api_key(key)
            log.write_asterix("API key disimpan dengan aman.")
            event.input.value = ""
            return

        # Input user normal
        log.write_user(command)
        session.append_history("user", command)

        # Analisis input pakai core
        plan = core.analyze(command)
        session.append_history("system", f"Plan: {plan}")

        # Kalau butuh konfirmasi
        if plan.get("requires_confirmation"):
            log.write_asterix(f"Rencana: {plan['plan']}")
            log.write_asterix("Apakah mau dilanjutkan? (y/n)")
            # Konfirmasi belum di-handle, bisa ditambah state machine nanti
        else:
            # Eksekusi langsung
            result = core.execute_plan(plan)
            log.write_asterix(result)
            session.append_history("assistant", result)

        # Reset input field
        event.input.value = ""


if __name__ == "__main__":
    app = AsterixApp()
    app.run()
