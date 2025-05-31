# main.py - CLI Entry Point
import typer
import sys
from typing import Optional
from tracker import tasks, logs, focus, review, db
from rich.console import Console

console = Console()

def main():
    """🧠 Reflex - Terminal-Based AI Productivity Tracker"""
    # Initialize database on first run
    try:
        db.init_db()
    except Exception as e:
        console.print(f"[red]Error initializing database: {e}[/red]")
        return
    
    # Simple argument parsing to avoid Typer compatibility issues
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == "add":
            if len(sys.argv) < 3:
                console.print("[red]Usage: reflex add \"Your task\"[/red]")
                return
            task = " ".join(sys.argv[2:])
            tasks.add_task(task)
            console.print(f"✅ Added task: [green]{task}[/green]")
            
        elif command == "start":
            session_type = sys.argv[2] if len(sys.argv) > 2 else "focus"
            if session_type == "focus":
                focus.start_focus_session()
            else:
                console.print("[red]Unknown session type. Use 'focus'[/red]")
                
        elif command == "focus":
            # Allow both 'start focus' and just 'focus'
            focus.start_focus_session()
            
        elif command == "log":
            if len(sys.argv) < 3:
                console.print("[red]Usage: reflex log \"Your log entry\"[/red]")
                return
            entry = " ".join(sys.argv[2:])
            logs.add_log(entry)
            console.print(f"📝 Logged: [blue]{entry}[/blue]")
            
        elif command == "stats":
            show_stats()
            
        elif command == "review":
            # Enhanced review command with provider options
            provider_name = None
            model_name = None
            
            # Parse optional arguments
            if "--provider" in sys.argv:
                provider_idx = sys.argv.index("--provider")
                if provider_idx + 1 < len(sys.argv):
                    provider_name = sys.argv[provider_idx + 1]
            
            if "--model" in sys.argv:
                model_idx = sys.argv.index("--model")
                if model_idx + 1 < len(sys.argv):
                    model_name = sys.argv[model_idx + 1]
            
            review.generate_ai_review(provider_name, model_name)
            
        elif command == "providers":
            # New command to list available AI providers
            review.list_providers()
            
        elif command == "complete":
            if len(sys.argv) < 3:
                console.print("[red]Usage: reflex complete <task_id>[/red]")
                return
            try:
                task_id = int(sys.argv[2])
                tasks.complete_task(task_id)
                console.print(f"✅ Task {task_id} marked as completed!")
            except ValueError:
                console.print("[red]Task ID must be a number[/red]")
                
        elif command == "list":
            tasks.list_tasks()
            
        elif command in ["help", "--help", "-h"]:
            show_help()
            
        else:
            console.print(f"[red]Unknown command: {command}[/red]")
            show_help()
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def show_stats():
    """📊 Show tasks done today and time spent"""
    stats_data = db.get_daily_stats()
    
    from rich.table import Table
    table = Table(title="📊 Today's Productivity Stats")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Tasks Completed", str(stats_data['completed_tasks']))
    table.add_row("Tasks Pending", str(stats_data['pending_tasks']))
    table.add_row("Focus Sessions", str(stats_data['focus_sessions']))
    table.add_row("Total Focus Time", f"{stats_data['total_focus_time']} minutes")
    table.add_row("Log Entries", str(stats_data['log_entries']))
    
    console.print(table)

def show_help():
    """Show help information"""
    from rich.panel import Panel
    from rich.text import Text
    
    help_text = Text()
    help_text.append("🧠 Reflex - Terminal-Based AI Productivity Tracker\n", style="bold cyan")
    help_text.append("Reflect. Focus. Improve.\n\n", style="italic")
    
    help_text.append("COMMANDS:\n", style="bold yellow")
    help_text.append("  add \"task\"       📋 Add a task to your current day\n", style="green")
    help_text.append("  start focus       ⏱️  Start a focus session with timer\n", style="green")
    help_text.append("  focus             ⏱️  Start a focus session (shortcut)\n", style="green")
    help_text.append("  log \"entry\"       📖 Add to your daily work log\n", style="green")
    help_text.append("  stats             📊 Show tasks done today and time spent\n", style="green")
    help_text.append("  review            🤖 AI reviews your day and suggests improvements\n", style="green")
    help_text.append("  providers         🔧 List available AI providers\n", style="green")
    help_text.append("  complete <id>     ✅ Mark a task as completed\n", style="green")
    help_text.append("  list              📋 List all tasks for today\n", style="green")
    help_text.append("  help              ❓ Show this help message\n", style="green")
    
    help_text.append("\nAI REVIEW OPTIONS:\n", style="bold yellow")
    help_text.append("  review --provider openai      Use OpenAI (ChatGPT)\n", style="blue")
    help_text.append("  review --provider anthropic   Use Anthropic (Claude)\n", style="blue")
    help_text.append("  review --provider gemini      Use Google Gemini\n", style="blue")
    help_text.append("  review --provider ollama      Use Ollama (local)\n", style="blue")
    help_text.append("  review --model gpt-4          Specify model to use\n", style="blue")
    
    help_text.append("\nSETUP:\n", style="bold yellow")
    help_text.append("  Set environment variables in .env file:\n", style="magenta")
    help_text.append("  • OPENAI_API_KEY=your_key\n", style="magenta")
    help_text.append("  • ANTHROPIC_API_KEY=your_key\n", style="magenta")
    help_text.append("  • GEMINI_API_KEY=your_key\n", style="magenta")
    help_text.append("  • Or install Ollama for local AI\n", style="magenta")
    
    help_text.append("\nEXAMPLES:\n", style="bold yellow")
    help_text.append('  python main.py add "Write blog post"\n', style="blue")
    help_text.append('  python main.py focus\n', style="blue")
    help_text.append('  python main.py log "Fixed authentication bug"\n', style="blue")
    help_text.append('  python main.py review --provider anthropic\n', style="blue")
    help_text.append('  python main.py complete 1\n', style="blue")
    
    console.print(Panel(help_text, expand=False))

if __name__ == "__main__":
    main()