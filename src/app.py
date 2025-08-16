from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, TextLog
from . import config, session

class AsterixApp(App):
    """Aplikasi Textual utama untuk Asterix"""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TextLog(id="log", highlight=True, wrap=True)
        yield Input(placeholder="Ketik perintah bahasa alami...")
        yield Footer()

    def on_mount(self) -> None:
        log = self.query_one("#log", TextLog)
        api_key = config.get_api_key()
        if api_key:
            log.write("[bold blue]Asterix:[/bold blue] API key sudah terdeteksi, siap digunakan.")
        else:
            log.write("[bold red]Asterix:[/bold red] Belum ada API key, ketik ':setkey <YOUR_KEY>' untuk set.")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        log = self.query_one("#log", TextLog)
        command = event.value.strip()
        if not command:
            return

        if command.startswith(":setkey "):
            key = command.split(" ", 1)[1]
            config.set_api_key(key)
            log.write("[bold green]Asterix:[/bold green] API key disimpan dengan aman.")
        else:
            log.write(f"[bold green]You:[/bold green] {command}")
            session.append_history("user", command)
            # sementara dummy reply
            log.write(f"[bold blue]Asterix:[/bold blue] Aku mendengar '{command}', nanti aku proses ya.")

        event.input.value = ""
