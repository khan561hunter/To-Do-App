"""CLI interface for in-memory todo application.

This module handles all user interaction, menu display, and delegates to TaskService.
Follows clean architecture: CLI logic separated from business logic.
"""

from typing import List
from todo_app.models import Task
from todo_app.services import TaskService


class TodoCLI:
    """Command-line interface for todo application.

    Responsibilities:
        - Display menu and messages
        - Validate user input
        - Delegate to TaskService
        - Display success/error messages
    """

    def __init__(self, service: TaskService):
        """Initialize CLI with TaskService instance."""
        self.service = service

    def display_menu(self) -> None:
        """Display main menu with numbered options."""
        print("\n=== Todo Application ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Complete/Incomplete")
        print("6. Exit")
        print("=========================")

    def get_menu_choice(self) -> str:
        """Get and validate menu selection from user."""
        while True:
            choice = input("Select option (1-6): ").strip()

            if choice in ("1", "2", "3", "4", "5", "6"):
                return choice
            print("Invalid option. Please select 1-6.")

    def display_tasks(self, tasks: List[Task]) -> None:
        """Display all tasks with visual indicators.

        Args:
            tasks: List of Task objects to display.
        """
        if not tasks:
            print("\nNo tasks found. Create a task to get started!")
            return

        print("\nTasks:")
        for task in tasks:
            print(task.display())

    def add_task_handler(self) -> None:
        """Handle Add Task option."""
        print("\n--- Add Task ---")

        # Get task title
        title = input("Enter task title: ").strip()
        if not title:
            print("Task title cannot be empty.")
            return

        # Get task description (optional)
        description_input = input("Enter task description (optional, press Enter to skip): ").strip()
        description = description_input if description_input else None

        # Delegate to service
        try:
            task = self.service.add_task(title, description)
            print(f"\nTask created with ID: {task.id}")
        except ValueError as e:
            print(f"Error: {e}")

    def view_tasks_handler(self) -> None:
        """Handle View Tasks option."""
        print("\n--- View Tasks ---")
        tasks = self.service.get_all_tasks()
        self.display_tasks(tasks)

    def update_task_handler(self) -> None:
        """Handle Update Task option."""
        print("\n--- Update Task ---")

        # Get task ID
        task_id_input = input("Enter task ID to update: ").strip()
        if not task_id_input:
            print("Task ID is required.")
            return

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("Task ID must be a number.")
            return

        # Get new values (optional)
        new_title = input("Enter new title (press Enter to keep current): ").strip()
        new_description = input("Enter new description (press Enter to keep current): ").strip()

        # Delegate to service
        try:
            if new_title or new_description:
                # Convert empty strings to None for service
                title_param = new_title if new_title else None
                desc_param = new_description if new_description else None
                self.service.update_task(task_id, title_param, desc_param)
                print(f"\nTask {task_id} updated successfully.")
            else:
                print("No changes provided. Task remains unchanged.")
        except ValueError as e:
            print(f"Error: {e}")

    def delete_task_handler(self) -> None:
        """Handle Delete Task option."""
        print("\n--- Delete Task ---")

        # Get task ID
        task_id_input = input("Enter task ID to delete: ").strip()
        if not task_id_input:
            print("Task ID is required.")
            return

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("Task ID must be a number.")
            return

        # Confirm deletion
        confirmation = input(f"Delete task {task_id}? (y/n): ").strip().lower()
        if confirmation not in ("y", "yes"):
            print("Deletion cancelled.")
            return

        # Delegate to service
        try:
            self.service.delete_task(task_id)
            print(f"\nTask {task_id} deleted successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def toggle_complete_handler(self) -> None:
        """Handle Mark Complete/Incomplete option."""
        print("\n--- Mark Complete/Incomplete ---")

        # Get task ID
        task_id_input = input("Enter task ID to toggle: ").strip()
        if not task_id_input:
            print("Task ID is required.")
            return

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("Task ID must be a number.")
            return

        # Delegate to service
        try:
            task = self.service.toggle_complete(task_id)
            status = "Complete" if task.completed else "Incomplete"
            print(f"\nTask {task_id} marked as {status}.")
        except ValueError as e:
            print(f"Error: {e}")

    def exit_handler(self) -> None:
        """Handle Exit option."""
        print("\nExiting application.")

    def run(self) -> None:
        """Main application loop.

        Displays menu, processes user input, and loops until Exit selected.
        Handles KeyboardInterrupt gracefully.
        """
        try:
            while True:
                self.display_menu()
                choice = self.get_menu_choice()

                if choice == "1":
                    self.add_task_handler()
                elif choice == "2":
                    self.view_tasks_handler()
                elif choice == "3":
                    self.update_task_handler()
                elif choice == "4":
                    self.delete_task_handler()
                elif choice == "5":
                    self.toggle_complete_handler()
                elif choice == "6":
                    self.exit_handler()
                    break
        except KeyboardInterrupt:
            print("\nExiting application.")
