"""Main entry point for in-memory todo application.

This file initializes the application and starts the CLI loop.
All data is lost on program termination per constitution.
"""

from todo_app import TaskService, TodoCLI


def main() -> None:
    """Main application entry point."""
    # Initialize service and CLI
    service = TaskService()
    cli = TodoCLI(service)

    # Start application
    cli.run()


if __name__ == "__main__":
    main()
