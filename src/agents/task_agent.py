"""Task Agent - Manages task operations and business logic.

This agent is responsible for:
- Creating tasks
- Updating tasks
- Deleting tasks
- Toggling task completion
- Enforcing business rules

Does NOT handle input/output or storage directly.
Reusable for any project needing task management logic.
"""

from typing import Optional
from todo_app.models import Task
from agents.storage_agent import StorageAgent
from agents.validation_agent import ValidationAgent


class TaskAgent:
    """Task business logic agent.

    Single Responsibility: Manage task operations and business rules.
    Delegates storage to StorageAgent, validation to ValidationAgent.
    """

    def __init__(self, storage_agent: StorageAgent, validation_agent: ValidationAgent):
        """Initialize task agent with required dependencies.

        Args:
            storage_agent: Agent responsible for storage operations
            validation_agent: Agent responsible for input validation
        """
        self.storage = storage_agent
        self.validator = validation_agent

    def create_task(self, title: str, description: Optional[str] = None) -> tuple[bool, Optional[Task], Optional[str]]:
        """Create a new task.

        Args:
            title: Task title
            description: Optional task description

        Returns:
            Tuple of (success, task, error_message)
            - (True, task, None) if successful
            - (False, None, error_message) if failed
        """
        # Validate title
        is_valid, error = self.validator.validate_title(title)
        if not is_valid:
            return False, None, error

        # Validate description if provided
        if description:
            is_valid, error = self.validator.validate_description(description)
            if not is_valid:
                return False, None, error

        # Clean inputs
        clean_title = self.validator.clean_input(title)
        clean_description = self.validator.clean_input(description)

        # Create task
        task_id = self.storage.generate_id()
        task = Task(
            task_id=task_id,
            title=clean_title,
            description=clean_description,
            completed=False
        )

        # Save to storage
        self.storage.save(task)

        return True, task, None

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks.

        Returns:
            List of all tasks from storage
        """
        return self.storage.get_all()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a specific task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task if found, None otherwise
        """
        return self.storage.get_by_id(task_id)

    def update_task(
        self, task_id: int, new_title: Optional[str] = None, new_description: Optional[str] = None
    ) -> tuple[bool, Optional[Task], Optional[str]]:
        """Update an existing task.

        Args:
            task_id: Task identifier
            new_title: New title (None to keep current)
            new_description: New description (None to keep current)

        Returns:
            Tuple of (success, task, error_message)
            - (True, task, None) if successful
            - (False, None, error_message) if failed
        """
        # Check if task exists
        task = self.storage.get_by_id(task_id)
        if task is None:
            return False, None, f"Task with ID {task_id} not found."

        # Validate new title if provided
        if new_title is not None:
            is_valid, error = self.validator.validate_title(new_title)
            if not is_valid:
                return False, None, error
            task.title = self.validator.clean_input(new_title)

        # Validate new description if provided
        if new_description is not None:
            is_valid, error = self.validator.validate_description(new_description)
            if not is_valid:
                return False, None, error
            task.description = self.validator.clean_input(new_description)

        return True, task, None

    def delete_task(self, task_id: int) -> tuple[bool, Optional[str]]:
        """Delete a task.

        Args:
            task_id: Task identifier

        Returns:
            Tuple of (success, error_message)
            - (True, None) if successful
            - (False, error_message) if failed
        """
        # Check if task exists
        task = self.storage.get_by_id(task_id)
        if task is None:
            return False, f"Task with ID {task_id} not found."

        # Remove from storage
        self.storage.remove(task)

        return True, None

    def toggle_completion(self, task_id: int) -> tuple[bool, Optional[Task], Optional[str]]:
        """Toggle task completion status.

        Args:
            task_id: Task identifier

        Returns:
            Tuple of (success, task, error_message)
            - (True, task, None) if successful
            - (False, None, error_message) if failed
        """
        # Check if task exists
        task = self.storage.get_by_id(task_id)
        if task is None:
            return False, None, f"Task with ID {task_id} not found."

        # Toggle completion
        task.completed = not task.completed

        return True, task, None
