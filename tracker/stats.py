import os
from .db import get_daily_stats
from rich.console import Console
from rich.table import Table 
from tracker.github import get_commit_count

def show_stats():
    """Display productivity stats for today."""
    from rich.console import Console
    console = Console()
    
    console.print("📊 Productivity Stats for Today", style="bold green")
    
    # Show tasks done today and time spent
    stats_data = get_daily_stats()
    
    if not stats_data:
        console.print("No data available for today.", style="red")
        return
    
    # Get commit count from GitHub
    commits_made = get_commit_count(os.getenv("GITHUB_USERNAME"), os.getenv("GITHUB_TOKEN"))
    stats_data['commits'] = commits_made

    table = Table(title="📊 Today's Productivity Stats")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Tasks Completed", str(stats_data['completed_tasks']))
    table.add_row("Tasks Pending", str(stats_data['pending_tasks']))
    table.add_row("Focus Sessions", str(stats_data['focus_sessions']))
    table.add_row("Total Focus Time", f"{stats_data['total_focus_time']} minutes")
    table.add_row("Log Entries", str(stats_data['log_entries']))
    table.add_row("GitHub Commits", str(stats_data['commits']))

    console.print(table)