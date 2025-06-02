from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()
panel_width = 80

def show_help():
    # Title
    console.print("\n[bold cyan]🧠 Reflex – Productivity Tracker in Terminal[/bold cyan]\n")

    # Usage 
    usage_text = Text()
    usage_text.append("USAGE:\n", style="bold yellow")
    usage_text.append("  python main.py <command> [content]", style="green")
    console.print(usage_text)
    console.print()

    # Commands table
    commands_table = Table(show_header=False, box=None, padding=(0, 1))
    commands_table.add_column("Command", style="blue")
    commands_table.add_column("Description", style="white")

    commands_table.add_row('add "task"', "📋 Add a task to your current day")
    commands_table.add_row("focus", "⏱️ Start a focus session with timer")
    commands_table.add_row('log "entry"', "📝 Add to your daily work log")
    commands_table.add_row("complete <id>", "✅ Mark a task as completed")
    commands_table.add_row("list", "📋 List all tasks for today")
    commands_table.add_row("stats", "📊 Show productivity statistics")
    commands_table.add_row("review", "🤖 AI-powered daily review")
    commands_table.add_row("providers", "🔧 List supported AI providers")
    commands_table.add_row("track-commits", "🔗 Track today's GitHub commits")
    commands_table.add_row("help", "📚 Show help message")
    commands_table.add_row("full-help", "📖 Show this detailed help")

    console.print(Panel(commands_table, title="[bold]Commands[/bold]", border_style="blue", padding=(1, 2), title_align="left", expand=False))
    console.print()

    # Combined AI Options + Setup
    ai_config_text = Text()
    ai_config_text.append("OPTIONS:\n", style="bold yellow")
    ai_config_text.append("  --provider <openai | anthropic | gemini | ollama>\n", style="green")
    ai_config_text.append("  --model <model_name>\n", style="green")
    ai_config_text.append("\nSETUP:\n", style="bold yellow")
    ai_config_text.append("  Set keys in .env:\n", style="green")
    ai_config_text.append("    OPENAI_API_KEY=...\n", style="green")
    ai_config_text.append("    ANTHROPIC_API_KEY=...\n", style="green")
    ai_config_text.append("    GEMINI_API_KEY=...", style="green")
    console.print(Panel(ai_config_text, title="[bold]AI Configuration[/bold]", border_style="blue", expand=False, padding=(1, 2), title_align="left"))
    console.print()

    console.print("\n[bold]For more detailed help and examples, run:[/bold] [green]reflex full-help[/green]\n")

def show_full_help():
    console.clear()
    # Intro (no panel)
    console.print("\n[bold cyan]🧠 Reflex – Productivity Tracker in Terminal[/bold cyan]")
    console.print("Built for developers. Focus better. Reflect deeper. Work smarter.\n", style="dim")

    # Usage
    usage_text = Text()
    usage_text.append("USAGE:\n", style="bold yellow")
    usage_text.append("  python main.py <command> [content]", style="green")
    console.print(usage_text)
    console.print()

    # Commands in panel
    cmd_table = Table.grid(padding=(1, 7))
    cmd_table.add_column("Command", style="bold blue")
    cmd_table.add_column("Description", style="white")

    cmd_table.add_row("add \"task\"",        "Add a task to your current day")
    cmd_table.add_row("focus",              "Start a timed focus session")
    cmd_table.add_row("log \"entry\"",      "Log work done or thoughts")
    cmd_table.add_row("complete <id>",      "Mark task as completed")
    cmd_table.add_row("list",               "List all tasks for today")
    cmd_table.add_row("stats",              "View daily task/time stats")
    cmd_table.add_row("review",             "Generate AI review summary")
    cmd_table.add_row("providers",          "List supported AI providers")
    cmd_table.add_row("track-commits",      "Track today’s GitHub commits")
    cmd_table.add_row("help",               "Show basic help")
    cmd_table.add_row("full-help",          "Show extended help")

    console.print(Panel(cmd_table, title="Commands", padding=(1, 2), title_align="left", expand=False))
    console.print()

    # AI Setup Panel
    ai_text = Text()
    ai_text.append("Flags:\n", style="bold")
    ai_text.append("  --provider openai | anthropic | gemini | ollama\n", style="green")
    ai_text.append("  --model <model-name>\n", style="green")

    ai_text.append("\n.env Setup:\n", style="bold")
    ai_text.append("  OPENAI_API_KEY=...\n", style="green")
    ai_text.append("  ANTHROPIC_API_KEY=...\n", style="green")
    ai_text.append("  GEMINI_API_KEY=...\n", style="green")
    ai_text.append("  # Ollama runs locally (no key needed)\n", style="dim")

    console.print(Panel(ai_text, title="AI Options & Setup", border_style="blue", title_align="left", padding=(1, 2), expand=False))
    console.print()

    # Examples Panel
    ex_text = Text()
    ex_text.append("  python main.py add \"Write tests\"\n", style="green")
    ex_text.append("  python main.py log \"Debugged auth module\"\n", style="green")
    ex_text.append("  python main.py review --provider openai\n", style="green")
    ex_text.append("  python main.py stats\n", style="green")

    console.print(Panel(ex_text, title="Examples", title_align="left", border_style="blue", padding=(1, 5), expand=False))