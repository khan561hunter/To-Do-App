"""Todo application package.

Provides in-memory task management via CLI interface.
All data is lost on program termination per constitution.
"""

from todo_app.models import Task
from todo_app.services import TaskService
from todo_app.cli import TodoCLI

__all__ = ["Task", "TaskService", "TodoCLI"]
