import time
from .db import get_db_connection
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
import typer

console = Console()

def start_focus_session(duration_minutes: int = 25):
    """Start a focus session with timer (default: 25 minutes - Pomodoro)"""
    console.print(f"🎯 Starting {duration_minutes}-minute focus session...")
    console.print("Press Ctrl+C to stop early")
    
    duration_seconds = duration_minutes * 60
    start_time = time.time()
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("🧠 Focus Session Active", total=duration_seconds)
            
            for i in range(duration_seconds):
                time.sleep(1)
                progress.update(task, advance=1)
            
        # Session completed successfully
        actual_duration = duration_minutes
        console.print(f"🎉 Focus session completed! ({duration_minutes} minutes)")
        
    except KeyboardInterrupt:
        # Session stopped early
        elapsed_time = time.time() - start_time
        actual_duration = int(elapsed_time / 60)
        console.print(f"\n⏹️ Focus session stopped. Time focused: {actual_duration} minutes")
    
    # Save session to database
    if actual_duration > 0:
        save_focus_session(actual_duration)

def save_focus_session(duration: int):
    """Save focus session to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO focus_sessions (duration) VALUES (?)", (duration,))
    conn.commit()
    conn.close()