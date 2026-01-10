"""Display Agent - Handles all console output and formatting.

This agent is responsible for:
- Displaying menus
- Formatting and printing tasks
- Showing success/error messages
- No business logic or input handling

Reusable for any console project needing formatted output.
"""

from typing import List
from todo_app.models import Task


class DisplayAgent:
    """Console display agent for formatted output.

    Single Responsibility: Handle all visual output to the console.
    Does not process input or perform operations.
    """

    def show_menu(self) -> None:
        """Display the main application menu."""
        print("\n=== Todo Application ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Complete/Incomplete")
        print("6. Exit")
        print("=========================")

    def show_header(self, title: str) -> None:
        """Display a section header.

        Args:
            title: Header text to display
        """
        print(f"\n--- {title} ---")

    def show_tasks(self, tasks: List[Task]) -> None:
        """Display all tasks with formatting.

        Args:
            tasks: List of Task objects to display
        """
        if not tasks:
            print("\nNo tasks found. Create a task to get started!")
            return

        print("\nTasks:")
        for task in tasks:
            print(task.display())

    def show_success(self, message: str) -> None:
        """Display a success message.

        Args:
            message: Success message to display
        """
        print(f"\n{message}")

    def show_error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: Error message to display
        """
        print(f"Error: {message}")

    def show_info(self, message: str) -> None:
        """Display an informational message.

        Args:
            message: Info message to display
        """
        print(f"{message}")

    def prompt_input(self, prompt_text: str) -> str:
        """Display a prompt and get user input.

        Args:
            prompt_text: Text to display as prompt

        Returns:
            User's input as string
        """
        return input(prompt_text).strip()

    def show_exit_message(self) -> None:
        """Display exit message when application closes."""
        print("\nExiting application. Goodbye!")

    def show_separator(self) -> None:
        """Display a visual separator line."""
        print("-" * 40)
