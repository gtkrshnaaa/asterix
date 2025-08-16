from textual.containers import VerticalScroll
from textual.widgets import Static 
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text

class ChatLog(VerticalScroll):
    """Wadah chat yang dapat di-scroll untuk menampilkan panel percakapan."""

    def write_user(self, message: str) -> None:
        """Menampilkan pesan dari pengguna dengan gaya."""
        panel = Panel(
            Text(message, justify="left"),
            title="[#84fab0]User",
            title_align="left",
            border_style="#84fab0",
            padding=(0, 1)
        )
        self.mount(Static(panel)) 
        self.scroll_end(animate=True)

    def write_asterix(self, message: str) -> None:
        """Menampilkan pesan teks sederhana dari Asterix."""
        panel = Panel(
            Text(message, justify="left"),
            title="[#86a8e7]Asterix",
            title_align="left",
            border_style="#86a8e7",
            padding=(0, 1)
        )
        self.mount(Static(panel)) 
        self.scroll_end(animate=True)

    def write_system(self, message: str) -> None:
        """Menampilkan pesan sistem."""
        panel = Panel(
            Text(message, justify="left", style="italic #f55a7f"),
            title="[#f55a7f]System",
            title_align="left",
            border_style="#f55a7f",
            padding=(0, 1)
        )
        self.mount(Static(panel)) 
        self.scroll_end(animate=True)
        
    def write_plan(self, plan_text: str, command: str | None = None) -> None:
        """Menampilkan rencana dan perintah dari Asterix dalam format yang rapi."""
        plan_renderable = Markdown(plan_text, style="#86a8e7")
        main_panel = Panel(
            plan_renderable,
            title="[bold #86a8e7]Asterix",
            title_align="left",
            border_style="#86a8e7",
            padding=(1, 2)
        )
        self.mount(Static(main_panel)) 
        
        if command:
            command_panel = Panel(
                Text(command, style="yellow"),
                title="[yellow]Command to Execute",
                title_align="left",
                border_style="yellow",
                padding=(0, 1)
            )
            self.mount(Static(command_panel)) 
        
        self.scroll_end(animate=True)

    def write_execution_result(self, result: str) -> None:
        """Menampilkan hasil eksekusi dalam panel."""
        result_panel = Panel(
            Text(result), 
            title="[#f55a7f]Execution Result", 
            border_style="#f55a7f",
            padding=(1,2)
        )
        self.mount(Static(result_panel)) 
        self.scroll_end(animate=True)