"""TaskService for in-memory todo application.

This module provides business logic and in-memory task storage.
All methods follow the service contract defined in contracts/service-contract.md.
"""


from typing import Optional, List
from todo_app.models import Task


class TaskService:
    """In-memory task service managing task lifecycle.

    Responsibilities:
        - Maintain in-memory task collection
        - Provide CRUD operations for tasks
        - Enforce business rules and validations
        - Manage auto-incrementing ID generation

    Raises:
        ValueError: When validation fails with human-readable message
    """

    def __init__(self):
        """Initialize task service with empty in-memory store."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Create and store new task with auto-generated ID.

        Args:
            title: Task title. Must be non-empty after strip().
            description: Task details. Can be None or non-empty string.

        Returns:
            Task: Newly created Task object with auto-generated ID.

        Raises:
            ValueError: If title is empty or whitespace-only.
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")

        # Validate length constraints
        if len(title) > 200:
            raise ValueError("Task title cannot exceed 200 characters.")

        if description and len(description) > 500:
            raise ValueError("Task description cannot exceed 500 characters.")

        # Clean description: convert empty string to None
        cleaned_description = description if description and description.strip() else None

        # Create new task with auto-generated ID
        task = Task(
            task_id=self._next_id,
            title=title.strip(),
            description=cleaned_description,
            completed=False,
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in storage.

        Returns:
            List[Task]: All Task objects in insertion order.
        """
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Return task by ID or None if not found.

        Args:
            task_id: Unique task identifier.

        Returns:
            Optional[Task]: Task object if found, None if ID doesn't exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(
        self, task_id: int, title: Optional[str] = None, description: Optional[str] = None
    ) -> Task:
        """Update task fields selectively. Only non-None parameters are updated.

        Args:
            task_id: Unique task identifier.
            title: New title. If None, title unchanged.
            description: New description. If None, description unchanged.

        Returns:
            Task: The updated Task object.

        Raises:
            ValueError: If task_id not found, or if title/description invalid.
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found.")

        # Update title if provided and non-None
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty.")
            if len(title) > 200:
                raise ValueError("Task title cannot exceed 200 characters.")
            task.title = title.strip()

        # Update description if provided (including None to clear it)
        if description is not None:
            cleaned_description = description if description and description.strip() else None
            if cleaned_description is not None and len(cleaned_description) > 500:
                raise ValueError("Task description cannot exceed 500 characters.")
            task.description = cleaned_description

        return task

    def delete_task(self, task_id: int) -> None:
        """Remove task from in-memory store permanently.

        Args:
            task_id: Unique task identifier.

        Returns:
            None

        Raises:
            ValueError: If task_id not found.
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found.")

        self._tasks.remove(task)

    def toggle_complete(self, task_id: int) -> Task:
        """Toggle completion status of a task (False <-> True).

        Args:
            task_id: Unique task identifier.

        Returns:
            Task: The updated Task object with toggled status.

        Raises:
            ValueError: If task_id not found.
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found.")

        task.completed = not task.completed
        return task
