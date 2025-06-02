from .db import get_db_connection
from datetime import date
from rich.console import Console

console = Console()

def add_log(entry: str):
    """Add a log entry"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (entry) VALUES (?)", (entry,))
    conn.commit()
    conn.close()

def get_today_logs():
    """Get today's log entries"""
    conn = get_db_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    
    cursor.execute(
        "SELECT entry, timestamp FROM logs WHERE date = ? ORDER BY timestamp", 
        (today,)
    )
    logs = cursor.fetchall()
    conn.close()
    return logs