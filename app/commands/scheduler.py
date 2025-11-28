# app/commands/scheduler.py
import time
import click
import schedule
from app.services.task_service import TaskService

def job_autoclose():
    service = TaskService()
    count = service.autoclose_overdue()
    print(f"[scheduler] autoclosed {count} tasks")

@click.command("run-scheduler")
@click.option("--interval-minutes", default=60, help="How often to run autoclose (minutes)")
def run_scheduler(interval_minutes):
    schedule.every(interval_minutes).minutes.do(job_autoclose)
    click.echo(f"Scheduler started: job runs every {interval_minutes} minutes. Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("Scheduler stopped.")

