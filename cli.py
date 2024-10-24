import click
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models.task import Task
from models.user import User
from datetime import datetime
import os

CURRENT_USER_FILE = "current_user.txt"

@click.group()
def cli():
    pass

@cli.command()
def init():
    """Initialize the database."""
    init_db()
    click.echo("Database initialized.")

@cli.command()
@click.option('--name', prompt='User name', help='The name of the user.')
def create_user(name):
    """Create a new user."""
    user = User.create(name=name)
    click.echo(f"User {name} created with id {user.id}")

@cli.command()
@click.option('--title', prompt='Task title', help='The title of the task.')
@click.option('--description', prompt='Task description', help='The description of the task.')
@click.option('--deadline', prompt='Task deadline (YYYY-MM-DD)', help='The deadline of the task.')
@click.option('--importance', prompt='Task importance', help='The importance of the task.')
@click.option('--estimated_time', prompt='Estimated time to complete', help='The estimated time to complete the task.')
@click.option('--user_id', prompt='User ID', help='The ID of the user.')
def create_task(title, description, deadline, importance, estimated_time, user_id):
    """Create a new task."""
    try:
        deadline_dt = datetime.strptime(deadline, '%Y-%m-%d')
    except ValueError:
        click.echo("Error: Deadline must be in YYYY-MM-DD format.")
        return

    task = Task.create(
        title=title,
        description=description,
        deadline=deadline_dt,
        importance=int(importance),
        estimated_time=int(estimated_time),
        user_id=int(user_id)
    )
    click.echo(f"Task {title} created with id {task.id}")

@cli.command()
def list_tasks():
    """List all tasks with their relevant information, sorted by importance (highest to lowest)."""
    tasks = Task.get_all()
    for task in sorted(tasks, key=lambda x: x.importance, reverse=True):
        user = User.find_by_id(task.user_id)
        user_name = user.name if user else "Unknown"
        click.echo(f"ID: {task.id} {task.title} | Importance: {task.importance} Description: {task.description} Deadline: {task.deadline} Time: {task.estimated_time} User: {user_name}")

@cli.command()
@click.option('--task_id', prompt='Task ID', help='The ID of the task to delete.')
def delete_task(task_id):
    """Delete a task by its ID."""
    if Task.delete(task_id):
        click.echo(f"Task with ID {task_id} has been deleted.")
    else:
        click.echo(f"Task with ID {task_id} not found.")

@cli.command()
@click.option('--user_id', prompt='User ID', help='The ID of the user to delete.')
def delete_user(user_id):
    """Delete a user by their ID."""
    if User.delete(user_id):
        click.echo(f"User with ID {user_id} has been deleted.")
    else:
        click.echo(f"User with ID {user_id} not found.")

@cli.command()
@click.option('--user_id', prompt='User ID', help='The ID of the user to switch to.')
def switch_user(user_id):
    """Switch to a different user by their ID."""
    user = User.find_by_id(user_id)
    if user:
        with open(CURRENT_USER_FILE, 'w') as f:
            f.write(str(user_id))
        click.echo(f"Switched to user with ID {user_id}.")
    else:
        click.echo(f"User with ID {user_id} not found.")

@cli.command()
def list_users():
    """List all users with their relevant information."""
    users = User.get_all()
    for user in users:
        click.echo(f"ID: {user.id}, Name: {user.name}")

@cli.command()
def main_menu():
    """Main menu loop to keep the user in the application until they choose to exit."""
    while True:
        click.echo("\nMain Menu:")
        click.echo("1. Create User")
        click.echo("2. Create Task")
        click.echo("3. List Tasks")
        click.echo("4. Delete Task")
        click.echo("5. Delete User")
        click.echo("6. Switch User")
        click.echo("7. List Users")
        click.echo("8. Exit")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            name = click.prompt("User name")
            create_user.main(['--name', name])
        elif choice == 2:
            title = click.prompt("Task title")
            description = click.prompt("Task description")
            deadline = click.prompt("Task deadline (YYYY-MM-DD)")
            importance = click.prompt("Task importance", type=int)
            estimated_time = click.prompt("Estimated time to complete", type=int)
            user_id = click.prompt("User ID", type=int)
            create_task.main(['--title', title, '--description', description, '--deadline', deadline, '--importance', str(importance), '--estimated_time', str(estimated_time), '--user_id', str(user_id)])
        elif choice == 3:
            list_tasks.main([])
        elif choice == 4:
            task_id = click.prompt("Task ID", type=int)
            delete_task.main(['--task_id', str(task_id)])
        elif choice == 5:
            user_id = click.prompt("User ID", type=int)
            delete_user.main(['--user_id', str(user_id)])
        elif choice == 6:
            user_id = click.prompt("User ID", type=int)
            switch_user.main(['--user_id', str(user_id)])
        elif choice == 7:
            list_users.main([])
        elif choice == 8:
            break
        else:
            click.echo("Invalid choice. Please try again.")

if __name__ == '__main__':
    cli()