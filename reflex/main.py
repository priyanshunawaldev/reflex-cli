import os
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from typing import Optional

from reflex.tracker import cli_help, tasks, logs, focus, review, db, github
from reflex.tracker.stats import show_stats

app = typer.Typer(
    help="🧠 Reflex - AI-Powered Terminal Productivity Tracker",
    rich_markup_mode="rich",
    invoke_without_command=True,
    add_completion=False,
)


console = Console()


@app.callback()
def main(ctx: typer.Context):
    try:
        db.init_db()
    except Exception as e:
        console.print(f"[red]Error initializing database: {e}[/red]")

    # If no command provided, show your custom help panel
    if ctx.invoked_subcommand is None:
        cli_help.show_help()
        raise typer.Exit()

@app.command("add")
def add_task(task: str):
    """📋 Add a task to your current day"""
    tasks.add_task(task)
    console.print(f"✅ Added task: [green]{task}[/green]")


@app.command("complete")
def complete(task_id: int):
    """✅ Mark a task as completed"""
    tasks.complete_task(task_id)
    console.print(f"✅ Task {task_id} marked as completed!")


@app.command("list-tasks")
def list_tasks():
    """📋 List all tasks for today"""
    tasks.list_tasks()


@app.command("start-focus")
def start_focus():
    """⏱️ Start a focus session with timer"""
    focus.start_focus_session()


@app.command("log")
def add_log(entry: str):
    """📖 Add to your daily work log"""
    logs.add_log(entry)
    console.print(f"📝 Logged: [blue]{entry}[/blue]")


@app.command("track-commits")
def track_commits():
    """🔗 Track today's GitHub commits"""
    username = os.getenv("GITHUB_USERNAME")
    token = os.getenv("GITHUB_TOKEN")

    if not username or not token:
        console.print("[red]Missing GitHub credentials.[/red]")
        username = Prompt.ask("Enter GitHub username")
        token = Prompt.ask("Enter GitHub token", password=True)

        if Confirm.ask("Save credentials to .env?"):
            with open(".env", "a") as f:
                f.write(f"GITHUB_USERNAME={username}\nGITHUB_TOKEN={token}\n")
            console.print("[green]Credentials saved.[/green]")

    github.track_commits(username, token)


@app.command("stats")
def stats():
    """📊 Show productivity statistics"""
    show_stats()


@app.command("review")
def ai_review(
    provider: Optional[str] = typer.Option(None, help="AI provider"),
    model: Optional[str] = typer.Option(None, help="Model name")
):
    """🤖 AI-powered daily review"""
    review.generate_ai_review(provider_name=provider, model_name=model)


@app.command("providers")
def list_providers():
    """🔧 List supported AI providers"""
    review.list_providers()


@app.command("help", hidden=True)
def show_short_help():
    """📚 Show help information"""
    cli_help.show_help()


@app.command("full-help", hidden=True)
def show_detailed_help():
    """📘 Show extended help information"""
    cli_help.show_full_help()


if __name__ == "__main__":
    app()
