# app/commands/autoclose_overdue.py
import click
from app.services.task_service import TaskService

@click.command("autoclose-overdue")
def autoclose_overdue():
    """Close overdue tasks (set status=done and closed_at)."""
    service = TaskService()
    count = service.autoclose_overdue()
    click.echo(f"Autoclosed {count} overdue tasks.")
