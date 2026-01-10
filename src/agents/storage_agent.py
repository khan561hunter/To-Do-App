"""Storage Agent - Manages in-memory task storage.

This agent is responsible for:
- Maintaining the task list in memory
- Providing CRUD-style storage operations
- Managing task ID generation
- Can be replaced later with file/database storage

Reusable for any console project needing in-memory storage.
"""

from typing import List, Optional
from todo_app.models import Task


class StorageAgent:
    """In-memory storage agent for tasks.

    Single Responsibility: Manage task storage and retrieval.
    No business logic, validation, or display logic.
    """

    def __init__(self):
        """Initialize empty in-memory storage."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def save(self, task: Task) -> None:
        """Save a new task to storage.

        Args:
            task: Task object to store
        """
        self._tasks.append(task)

    def get_all(self) -> List[Task]:
        """Retrieve all tasks from storage.

        Returns:
            Copy of all tasks in storage
        """
        return self._tasks.copy()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def remove(self, task: Task) -> None:
        """Remove a task from storage.

        Args:
            task: Task object to remove
        """
        self._tasks.remove(task)

    def generate_id(self) -> int:
        """Generate next unique ID for a task.

        Returns:
            Next available unique ID
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def exists(self, task_id: int) -> bool:
        """Check if a task exists by ID.

        Args:
            task_id: Task identifier to check

        Returns:
            True if task exists, False otherwise
        """
        return self.get_by_id(task_id) is not None
