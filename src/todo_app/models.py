"""Task model for in-memory todo application.

This module defines the Task entity used throughout the application.
Tasks are stored in-memory and lost on program termination per constitution.
"""


class Task:
    """Represents a todo item with auto-generated unique identifier.

    Attributes:
        id (int): Auto-generated unique identifier
        title (str): Required task title
        description (Optional[str]): Optional task details
        completed (bool): Completion status (default: False)
    """

    def __init__(self, task_id: int, title: str, description: str | None = None, completed: bool = False):
        """Initialize a new Task.

        Args:
            task_id: Auto-generated unique identifier
            title: Required task title (non-empty after strip)
            description: Optional task details (can be None)
            completed: Completion status (default: False)
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed

    def __repr__(self) -> str:
        """Return string representation of Task for debugging."""
        status_icon = "[✓]" if self.completed else "[ ]"
        desc_str = f" - {self.description}" if self.description else ""
        return f"Task(id={self.id}, title={self.title!r}, completed={self.completed})"

    def display(self) -> str:
        """Return formatted string for console display.

        Returns:
            Formatted task string with status icon.
        """
        status_icon = "[✓]" if self.completed else "[ ]"
        desc_str = f"\n      Description: {self.description}" if self.description else ""
        return f"[{self.id}] {self.title} ({status_icon}){desc_str}"
