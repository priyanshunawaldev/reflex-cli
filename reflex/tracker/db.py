import sqlite3
import json
from datetime import datetime, date
from pathlib import Path
import os

DB_PATH = Path.home() / ".reflex" / "reflex.db"

def init_db():
    """Initialize the SQLite database"""
    # Ensure parent directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            date_added DATE DEFAULT CURRENT_DATE,
            date_completed DATE
        )
    ''')
    
    # Focus sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS focus_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration INTEGER NOT NULL,
            date DATE DEFAULT CURRENT_DATE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry TEXT NOT NULL,
            date DATE DEFAULT CURRENT_DATE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

def get_daily_stats():
    """Get today's productivity statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    
    # Get task stats
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE date_added = ? AND completed = 1", (today,))
    completed_tasks = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE date_added = ? AND completed = 0", (today,))
    pending_tasks = cursor.fetchone()[0]
    
    # Get focus session stats
    cursor.execute("SELECT COUNT(*), SUM(duration) FROM focus_sessions WHERE date = ?", (today,))
    focus_data = cursor.fetchone()
    focus_sessions = focus_data[0] or 0
    total_focus_time = focus_data[1] or 0
    
    # Get log entries count
    cursor.execute("SELECT COUNT(*) FROM logs WHERE date = ?", (today,))
    log_entries = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'focus_sessions': focus_sessions,
        'total_focus_time': total_focus_time,
        'log_entries': log_entries
    }