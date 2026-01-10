"""Main entry point for agent-based Todo application.

This file demonstrates the agent-based architecture:
- Main agent (TodoAppAgent) orchestrates everything
- All functionality delegated to specialized sub-agents
- Clean separation of concerns
"""

from agents import TodoAppAgent


def main() -> None:
    """Main application entry point using agent architecture."""
    # Create and start the main agent
    app = TodoAppAgent()
    app.start()


if __name__ == "__main__":
    main()
