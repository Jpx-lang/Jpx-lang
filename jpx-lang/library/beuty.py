"""
beuty - Module untuk mempercantik tampilan terminal JPX
Menggunakan library Rich untuk warna dan formatting
"""

import os
import sys
from datetime import datetime

# Cek ketersediaan Rich
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich import inspect
    from rich.markdown import Markdown
    from rich.rule import Rule
    from rich.columns import Columns
    from rich.text import Text
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    # Fallback simple print
    def rprint(*args, **kwargs):
        print(*args)

class Beuty:
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
    
    def is_available(self):
        """Cek apakah Rich terinstall"""
        return RICH_AVAILABLE
    
    # ========== LEVEL PRINT ==========
    def print(self, text):
        """Print biasa"""
        if RICH_AVAILABLE:
            self.console.print(text)
        else:
            print(text)
    
    def success(self, text):
        """Print sukses (hijau)"""
        if RICH_AVAILABLE:
            self.console.print(f"✓ {text}", style="bold green")
        else:
            print(f"[SUCCESS] {text}")
    
    def error(self, text):
        """Print error (merah)"""
        if RICH_AVAILABLE:
            self.console.print(f"✗ {text}", style="bold red")
        else:
            print(f"[ERROR] {text}")
    
    def warn(self, text):
        """Print warning (kuning)"""
        if RICH_AVAILABLE:
            self.console.print(f"⚠ {text}", style="bold yellow")
        else:
            print(f"[WARN] {text}")
    
    def info(self, text):
        """Print info (biru)"""
        if RICH_AVAILABLE:
            self.console.print(f"ℹ {text}", style="bold blue")
        else:
            print(f"[INFO] {text}")
    
    def debug(self, text):
        """Print debug (magenta)"""
        if RICH_AVAILABLE:
            self.console.print(f"🔍 {text}", style="dim magenta")
        else:
            print(f"[DEBUG] {text}")
    
    # ========== FORMATTING ==========
    def panel(self, text, title=""):
        """Teks dalam panel"""
        if RICH_AVAILABLE:
            panel = Panel(text, title=title, border_style="bright_blue")
            self.console.print(panel)
        else:
            print(f"\n--- {title} ---\n{text}\n---")
    
    def rule(self, title=""):
        """Garis pemisah"""
        if RICH_AVAILABLE:
            rule = Rule(title, style="bright_blue")
            self.console.print(rule)
        else:
            print("-" * 50 + " " + title + " " + "-" * 50)
    
    # ========== TABLE ==========
    def table(self, headers, rows):
        """Buat tabel dengan header dan rows"""
        if not RICH_AVAILABLE:
            # Fallback simple
            print(" | ".join(headers))
            print("-" * 50)
            for row in rows:
                print(" | ".join([str(x) for x in row]))
            return
        
        table = Table(show_header=True, header_style="bold cyan")
        for header in headers:
            table.add_column(header)
        
        for row in rows:
            table.add_row(*[str(x) for x in row])
        
        self.console.print(table)
    
    # ========== PROGRESS ==========
    def progress(self, total=100, description="Processing"):
        """Buat progress bar (return progress object)"""
        if not RICH_AVAILABLE:
            print(f"{description}...")
            return None
        
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        return progress
    
    def progress_start(self, progress, description="Processing", total=100):
        """Mulai progress task"""
        if progress:
            task = progress.add_task(description, total=total)
            progress.start()
            return task
        return None
    
    def progress_update(self, progress, task, advance=1):
        """Update progress"""
        if progress and task is not None:
            progress.update(task, advance=advance)
    
    def progress_stop(self, progress):
        """Hentikan progress"""
        if progress:
            progress.stop()
    
    # ========== SPINNER ==========
    def spinner(self, text="Loading..."):
        """Buat spinner"""
        if not RICH_AVAILABLE:
            print(text)
            return None
        
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        )
        task = progress.add_task(text, total=None)
        progress.start()
        return progress, task
    
    def spinner_stop(self, progress):
        """Hentikan spinner"""
        if progress:
            progress.stop()
    
    # ========== INPUT ==========
    def input(self, prompt_text, default=""):
        """Input dengan prompt"""
        if not RICH_AVAILABLE:
            if default:
                user_input = input(f"{prompt_text} ({default}): ")
                return user_input if user_input else default
            return input(f"{prompt_text}: ")
        
        return Prompt.ask(prompt_text, default=default)
    
    def confirm(self, prompt_text, default=True):
        """Konfirmasi ya/tidak"""
        if not RICH_AVAILABLE:
            default_str = "Y/n" if default else "y/N"
            response = input(f"{prompt_text} ({default_str}): ")
            if not response:
                return default
            return response.lower() in ('y', 'yes')
        
        return Confirm.ask(prompt_text, default=default)
    
    def choose(self, prompt_text, choices, default=None):
        """
        Pilih dari daftar pilihan
        Args:
            prompt_text: Teks pertanyaan
            choices: List pilihan
            default: Pilihan default (opsional)
        Returns:
            Pilihan yang dipilih
        """
        if not RICH_AVAILABLE:
            print(prompt_text)
            for i, choice in enumerate(choices):
                default_mark = " (default)" if default and choice == default else ""
                print(f"  {i+1}. {choice}{default_mark}")
            
            while True:
                try:
                    idx_str = input("Pilih nomor: ")
                    if not idx_str and default:
                        return default
                    idx = int(idx_str) - 1
                    if 0 <= idx < len(choices):
                        return choices[idx]
                    print(f"Pilihan harus 1-{len(choices)}")
                except ValueError:
                    print("Masukkan angka")
        
        return Prompt.ask(prompt_text, choices=choices, default=default)
    
    # ========== MARKDOWN ==========
    def markdown(self, text):
        """Render markdown"""
        if RICH_AVAILABLE:
            md = Markdown(text)
            self.console.print(md)
        else:
            print(text)
    
    # ========== CODE HIGHLIGHT ==========
    def code(self, text, language="python"):
        """Tampilkan kode dengan highlight"""
        if RICH_AVAILABLE:
            syntax = Syntax(text, language, theme="monokai")
            self.console.print(syntax)
        else:
            print(text)
    
    # ========== INSPECT ==========
    def inspect(self, obj):
        """Inspeksi objek"""
        if RICH_AVAILABLE:
            inspect(obj)
        else:
            print(obj)
    
    # ========== COLUMNS ==========
    def columns(self, items):
        """Tampilkan item dalam kolom"""
        if RICH_AVAILABLE:
            col = Columns(items)
            self.console.print(col)
        else:
            for item in items:
                print(f"• {item}")
    
    # ========== CLEAR ==========
    def clear(self):
        """Bersihkan layar"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # ========== TIMESTAMP ==========
    def timestamp(self):
        """Dapatkan timestamp"""
        return datetime.now().strftime("%H:%M:%S")
    
    def date(self):
        """Dapatkan tanggal"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def datetime(self):
        """Dapatkan tanggal dan waktu"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Ekspor instance beuty
exports = {
    'beuty': Beuty()
}