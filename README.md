# Task Prioritization Assistant

## Description
A Python app that takes in a list of tasks and helps you prioritize them based on deadlines, importance, and estimated time to complete. It can send reminders or break tasks into smaller, manageable chunks to keep you on track.

## Requirements
- Python 3.8.13
- SQLAlchemy
- Click

## Installation
1. Clone the repository.
2. Install dependencies using `pipenv install`.

## Usage
1. Initialize the database:
    ```sh
    python cli.py init
    ```
2. Start the main menu:
    ```sh
    python cli.py main-menu
    ```

### Individual Commands
1. Create a user:
    ```sh
    python cli.py create-user --name "John Doe"
    ```
2. Create a task:
    ```sh
    python cli.py create-task --title "Task 1" --description "Description" --deadline "2023-12-31" --importance 5 --estimated_time 120 --user_id 1
    ```
3. List all tasks sorted by importance:
    ```sh
    python cli.py list-tasks
    ```
4. Delete a task by its ID:
    ```sh
    python cli.py delete-task --task_id 1
    ```
5. Delete a user by their ID:
    ```sh
    python cli.py delete-user --user_id 1
    ```
6. Switch to a different user by their ID:
    ```sh
    python cli.py switch-user --user_id 1
    ```
7. List all users:
    ```sh
    python cli.py list-users
    ```

## Project Structure
- `models/`: Contains ORM models.
- `cli.py`: Contains CLI commands.
- `database.py`: Database setup and initialization.
- `Pipfile`: Project dependencies.
- `README.md`: Project description and usage.