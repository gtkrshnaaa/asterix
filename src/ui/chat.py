from textual.widgets import Log

class ChatLog(Log):
    """Widget log khusus untuk menampilkan percakapan."""

    def __init__(self, **kwargs):
        super().__init__(highlight=True, **kwargs)

    def write_user(self, message: str) -> None:
        """Menampilkan pesan dari pengguna."""
        self.write(f"[bold #84fab0]User >[/] {message}")

    def write_asterix(self, message: str) -> None:
        """Menampilkan pesan dari Asterix."""
        self.write(f"[bold #86a8e7]Asterix >[/] {message}")

    def write_system(self, message: str) -> None:
        """Menampilkan pesan sistem (misalnya rencana atau error)."""
        self.write(f"[italic #f55a7f]System > {message}[/]")