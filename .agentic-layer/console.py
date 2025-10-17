"""Shared Rich Console instance and formatting utilities for ADW.

This module provides a singleton Rich Console instance and helper functions
for consistent styling across all ADW modules.
"""
# /// script
# dependencies = [
#   "rich",
# ]
# ///

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Singleton console instance
console = Console()

# Color scheme
COLORS = {
    "phase": "cyan",
    "step": "blue",
    "success": "green",
    "error": "red",
    "warning": "yellow",
    "info": "white"
}

def phase_header(phase_name: str, phase_num: int, total: int) -> Panel:
    """Create a styled panel for phase headers."""
    title = Text(
        f"PHASE {phase_num}/{total}: {phase_name.upper()}",
        style=f"bold {COLORS['phase']}"
    )
    return Panel(title, border_style=COLORS['phase'])

def step_info(step_num: int, message: str):
    """Print a styled step message."""
    console.print(f"[{COLORS['step']}]Step {step_num}:[/{COLORS['step']}] {message}")

def success(message: str):
    """Print a success message."""
    console.print(f"[{COLORS['success']}]✓[/{COLORS['success']}] {message}")

def error(message: str):
    """Print an error message."""
    console.print(f"[{COLORS['error']}]✗[/{COLORS['error']}] {message}", style="bold")

def warning(message: str):
    """Print a warning message."""
    console.print(f"[{COLORS['warning']}]⚠[/{COLORS['warning']}] {message}")
