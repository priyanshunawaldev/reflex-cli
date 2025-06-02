from reflex.tracker.db import get_db_connection
from datetime import date
import datetime
from rich.console import Console
from rich.table import Table
from .security import clean_user_input, is_reasonable_input

console = Console()

def add_task(task: str):
    """Add a new task"""
    # Quick validation - better than nothing
    if not is_reasonable_input(task):
        console.print("[red]Task looks suspicious or too long. Try something simpler.[/red]")
        return
    
    clean_task = clean_user_input(task)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (clean_task,))
    conn.commit()
    conn.close()

def complete_task(task_id: int):
    """Mark a task as completed"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET completed = 1, date_completed = ? WHERE id = ?", 
        (date.today().isoformat(), task_id)
    )
    conn.commit()
    conn.close()

def list_tasks():
    """List all tasks for today"""
    conn = get_db_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    
    cursor.execute(
        "SELECT id, task, completed FROM tasks WHERE date_added = ? ORDER BY id", 
        (today,)
    )
    tasks = cursor.fetchall()
    conn.close()
    
    if not tasks:
        console.print("📋 No tasks for today. Add one with: [cyan]reflex add \"Your task\"[/cyan]")
        return
    
    table = Table(title="📋 Today's Tasks")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Task", style="white")
    table.add_column("Status", style="green", width=12)
    
    for task_id, task, completed in tasks:
        status = "✅ Done" if completed else "⏳ Pending"
        status_style = "green" if completed else "yellow"
        table.add_row(str(task_id), task, f"[{status_style}]{status}[/{status_style}]")
    
    console.print(table)