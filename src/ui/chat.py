from textual.widgets import Log


class ChatLog(Log):
    """Widget log khusus untuk chat."""

    def __init__(self, **kwargs):
        # hapus wrap, hanya highlight yang valid
        super().__init__(highlight=True, **kwargs)

    def write_user(self, message: str) -> None:
        self.write(f"[bold green]User:[/bold green] {message}")

    def write_asterix(self, message: str) -> None:
        self.write(f"[bold blue]Asterix:[/bold blue] {message}")
