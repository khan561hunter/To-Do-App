"""Main Controller Agent - TodoApp Main Agent.

This agent is responsible for:
- Starting the application
- Running the main application loop
- Delegating all tasks to sub-agents
- Handling application lifecycle

NEVER handles business logic, input/output, or storage directly.
Reusable pattern for any console application.
"""

from agents.storage_agent import StorageAgent
from agents.validation_agent import ValidationAgent
from agents.display_agent import DisplayAgent
from agents.task_agent import TaskAgent
from agents.command_router_agent import CommandRouterAgent


class TodoAppAgent:
    """Main controller agent for the Todo application.

    Single Responsibility: Orchestrate application flow and coordinate sub-agents.
    All functionality is delegated to specialized sub-agents.
    """

    def __init__(self):
        """Initialize the main agent and all sub-agents."""
        # Initialize all sub-agents
        self.storage_agent = StorageAgent()
        self.validation_agent = ValidationAgent()
        self.display_agent = DisplayAgent()
        self.task_agent = TaskAgent(self.storage_agent, self.validation_agent)
        self.router_agent = CommandRouterAgent(
            self.task_agent,
            self.display_agent,
            self.validation_agent
        )

    def start(self) -> None:
        """Start the application and run the main loop.

        Handles:
        - Main application loop
        - Menu display and choice validation
        - Command routing
        - Graceful exit on Ctrl+C
        """
        try:
            while True:
                # Display menu via display agent
                self.display_agent.show_menu()

                # Get user choice
                choice = self._get_validated_choice()

                # Route command to appropriate handler
                should_continue = self.router_agent.route_command(choice)

                # Exit if user chose exit option
                if not should_continue:
                    self.display_agent.show_exit_message()
                    break

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            self.display_agent.show_exit_message()

    def _get_validated_choice(self) -> str:
        """Get and validate menu choice from user.

        Returns:
            Valid menu choice (1-6)
        """
        while True:
            choice = self.display_agent.prompt_input("Select option (1-6): ")

            # Validate choice
            is_valid, error = self.validation_agent.validate_menu_choice(choice, 1, 6)

            if is_valid:
                return choice

            # Show error and retry
            self.display_agent.show_error(error)
