from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn


class Display:
    def __init__(self):
        self.console = Console()

    def banner(self):
        ascii_art = r"""
 ___              _____    ___                    _
| _ \___ _ __  __|_   _|__| _ \_ _ ___ _ __  _ __| |_
|   / -_) '_ \/ _ \| |/ _ \  _/ '_/ _ \ '  \| '_ \  _|
|_|_\___| .__/\___/|_|\___/_| |_| \___/_|_|_| .__/\__|
        """
        self.console.print(Panel(ascii_art, style="bold cyan", subtitle="[bold white]v1.0.0[/bold white]"))

    def show_help(self):
        self.banner()
        self.console.print("\n[bold yellow]USAGE:[/bold yellow] [green]RepoToPrompt[/green] [path] [options]\n")
        
        table = Table(show_header=True, header_style="bold magenta", box=None)
        table.add_column("Option", style="cyan")
        table.add_column("Description")
        
        table.add_row("--init-ignore", "Initialize a default .RepoToPromptignore file.")
        table.add_row("--force", "Overwrite existing ignore file with --init-ignore.")
        table.add_row("-o, --output", "Output filename (default: output.txt).")
        table.add_row("-h, --help", "Show this styled help page.")
        
        self.console.print(table)

    def summary(self, stats, output_path):
        table = Table(title="Processing Summary", show_header=False, border_style="dim")
        table.add_row("Files Processed", f"[bold green]{stats['processed']}[/bold green]")
        table.add_row("Files Ignored", f"[yellow]{stats['ignored']}[/yellow]")
        table.add_row("Resulting File", f"[bold cyan]{output_path}[/bold cyan]")
        self.console.print(table)

    def success(self, msg): self.console.print(f"[bold green]✔[/bold green] {msg}")
    def info(self, msg): self.console.print(f"[bold blue]ℹ[/bold blue] {msg}")
    def error(self, msg): self.console.print(f"[bold red]✘ ERROR:[/bold red] {msg}")
    def warning(self, msg): self.console.print(f"[bold yellow]⚠ WARNING:[/bold yellow] {msg}")

    def progress_context(self):
        """Returns a configured Progress context manager."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console,
            transient=False
        )