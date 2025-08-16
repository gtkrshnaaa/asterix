from textual.widgets import TextLog

class ChatLog(TextLog):
    """Widget log obrolan Asterix"""
    def __init__(self, **kwargs):
        super().__init__(highlight=True, wrap=True, **kwargs)

    def write_user(self, message: str):
        self.write(f"[bold green]You:[/bold green] {message}")

    def write_asterix(self, message: str):
        self.write(f"[bold blue]Asterix:[/bold blue] {message}")
