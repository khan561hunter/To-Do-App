"""Agents package - Reusable agent-based architecture.

This package contains all agents for the Todo application:
- TodoAppAgent: Main controller agent
- CommandRouterAgent: Routes commands to handlers
- TaskAgent: Manages task business logic
- StorageAgent: Handles in-memory storage
- ValidationAgent: Validates user input
- DisplayAgent: Handles console output

Each agent has a single responsibility and can be reused in other projects.
"""

from agents.todo_app_agent import TodoAppAgent
from agents.command_router_agent import CommandRouterAgent
from agents.task_agent import TaskAgent
from agents.storage_agent import StorageAgent
from agents.validation_agent import ValidationAgent
from agents.display_agent import DisplayAgent

__all__ = [
    "TodoAppAgent",
    "CommandRouterAgent",
    "TaskAgent",
    "StorageAgent",
    "ValidationAgent",
    "DisplayAgent",
]
