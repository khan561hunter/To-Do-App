"""Command Router Agent - Routes user commands to appropriate handlers.

This agent is responsible for:
- Mapping user menu choices to actions
- Calling the appropriate sub-agents
- Collecting input from display agent
- Returning results to the main controller

Does NOT perform business logic or display operations directly.
Reusable for any console project needing command routing.
"""

from agents.task_agent import TaskAgent
from agents.display_agent import DisplayAgent
from agents.validation_agent import ValidationAgent


class CommandRouterAgent:
    """Command routing agent for menu-driven applications.

    Single Responsibility: Route user commands to appropriate handlers.
    Coordinates between display, validation, and task agents.
    """

    def __init__(
        self,
        task_agent: TaskAgent,
        display_agent: DisplayAgent,
        validation_agent: ValidationAgent
    ):
        """Initialize router with required agent dependencies.

        Args:
            task_agent: Agent handling task operations
            display_agent: Agent handling display operations
            validation_agent: Agent handling validation
        """
        self.task_agent = task_agent
        self.display = display_agent
        self.validator = validation_agent

    def route_command(self, choice: str) -> bool:
        """Route a menu choice to the appropriate handler.

        Args:
            choice: User's menu selection (1-6)

        Returns:
            True to continue running, False to exit
        """
        if choice == "1":
            self._handle_add_task()
        elif choice == "2":
            self._handle_view_tasks()
        elif choice == "3":
            self._handle_update_task()
        elif choice == "4":
            self._handle_delete_task()
        elif choice == "5":
            self._handle_toggle_complete()
        elif choice == "6":
            return False  # Signal to exit
        return True  # Continue running

    def _handle_add_task(self) -> None:
        """Handle the Add Task command."""
        self.display.show_header("Add Task")

        # Get title from user
        title = self.display.prompt_input("Enter task title: ")
        if not title:
            self.display.show_error("Task title cannot be empty.")
            return

        # Get optional description
        description = self.display.prompt_input("Enter task description (optional, press Enter to skip): ")

        # Create task via task agent
        success, task, error = self.task_agent.create_task(title, description)

        if success:
            self.display.show_success(f"Task created with ID: {task.id}")
        else:
            self.display.show_error(error)

    def _handle_view_tasks(self) -> None:
        """Handle the View Tasks command."""
        self.display.show_header("View Tasks")

        # Get all tasks from task agent
        tasks = self.task_agent.get_all_tasks()

        # Display via display agent
        self.display.show_tasks(tasks)

    def _handle_update_task(self) -> None:
        """Handle the Update Task command."""
        self.display.show_header("Update Task")

        # Get task ID from user
        task_id_input = self.display.prompt_input("Enter task ID to update: ")

        # Validate task ID
        is_valid, task_id, error = self.validator.validate_task_id(task_id_input)
        if not is_valid:
            self.display.show_error(error)
            return

        # Check if task exists
        if not self.task_agent.get_task(task_id):
            self.display.show_error(f"Task with ID {task_id} not found.")
            return

        # Get new values
        new_title = self.display.prompt_input("Enter new title (press Enter to keep current): ")
        new_description = self.display.prompt_input("Enter new description (press Enter to keep current): ")

        # Only update if at least one field provided
        if not new_title and not new_description:
            self.display.show_info("No changes provided. Task remains unchanged.")
            return

        # Convert empty strings to None
        title_param = new_title if new_title else None
        desc_param = new_description if new_description else None

        # Update task via task agent
        success, task, error = self.task_agent.update_task(task_id, title_param, desc_param)

        if success:
            self.display.show_success(f"Task {task_id} updated successfully.")
        else:
            self.display.show_error(error)

    def _handle_delete_task(self) -> None:
        """Handle the Delete Task command."""
        self.display.show_header("Delete Task")

        # Get task ID from user
        task_id_input = self.display.prompt_input("Enter task ID to delete: ")

        # Validate task ID
        is_valid, task_id, error = self.validator.validate_task_id(task_id_input)
        if not is_valid:
            self.display.show_error(error)
            return

        # Get confirmation
        confirmation = self.display.prompt_input(f"Delete task {task_id}? (y/n): ")
        if not self.validator.validate_confirmation(confirmation):
            self.display.show_info("Deletion cancelled.")
            return

        # Delete task via task agent
        success, error = self.task_agent.delete_task(task_id)

        if success:
            self.display.show_success(f"Task {task_id} deleted successfully.")
        else:
            self.display.show_error(error)

    def _handle_toggle_complete(self) -> None:
        """Handle the Toggle Complete/Incomplete command."""
        self.display.show_header("Mark Complete/Incomplete")

        # Get task ID from user
        task_id_input = self.display.prompt_input("Enter task ID to toggle: ")

        # Validate task ID
        is_valid, task_id, error = self.validator.validate_task_id(task_id_input)
        if not is_valid:
            self.display.show_error(error)
            return

        # Toggle completion via task agent
        success, task, error = self.task_agent.toggle_completion(task_id)

        if success:
            status = "Complete" if task.completed else "Incomplete"
            self.display.show_success(f"Task {task_id} marked as {status}.")
        else:
            self.display.show_error(error)
