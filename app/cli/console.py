# app/cli/console.py
import click
from app.commands.autoclose_overdue import autoclose_overdue
from app.commands.scheduler import run_scheduler
from app.services.task_service import TaskService
from app.services.project_service import ProjectService
from datetime import datetime

@click.group()
def cli():
    pass

@cli.command("create-project")
@click.argument("name")
@click.option("--description", default=None)
def create_project(name, description):
    service = ProjectService()
    p = service.create_project(name=name, description=description)
    click.echo(f"Created project {p.id} - {p.name}")

@cli.command("list-projects")
def list_projects():
    service = ProjectService()
    projects = service.list_projects()
    for p in projects:
        click.echo(f"{p.id}: {p.name} - {p.description}")

@cli.command("create-task")
@click.argument("title")
@click.option("--description", default=None)
@click.option("--deadline", default=None, help="Deadline as YYYY-MM-DDTHH:MM (UTC)")
@click.option("--project-id", default=None, type=int)
def create_task(title, description, deadline, project_id):
    from datetime import datetime
    dl = None
    if deadline:
        dl = datetime.fromisoformat(deadline)
    service = TaskService()
    t = service.create_task(title=title, description=description, deadline=dl, project_id=project_id)
    click.echo(f"Created task {t.id} - {t.title}")

@cli.command("list-tasks")
@click.option("--project-id", default=None, type=int)
def list_tasks(project_id):
    service = TaskService()
    tasks = service.list_tasks(project_id=project_id)
    for t in tasks:
        click.echo(f"{t.id}: [{t.status}] {t.title} (project={t.project_id}) deadline={t.deadline} closed_at={t.closed_at}")

# register imported commands
cli.add_command(autoclose_overdue)
cli.add_command(run_scheduler)
