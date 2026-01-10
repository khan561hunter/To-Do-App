"""Validation Agent - Validates user input and commands.

This agent is responsible for:
- Validating user input (empty strings, valid IDs, etc.)
- Checking data constraints (length limits)
- Returning clean error messages
- No business logic or storage operations

Reusable for any console project needing input validation.
"""

from typing import Optional, Tuple


class ValidationAgent:
    """Input validation agent for user commands and data.

    Single Responsibility: Validate all user inputs and return error messages.
    Does not perform operations, only validates.
    """

    # Validation rules (can be configured)
    MAX_TITLE_LENGTH = 200
    MAX_DESCRIPTION_LENGTH = 500

    def validate_title(self, title: Optional[str]) -> Tuple[bool, Optional[str]]:
        """Validate task title.

        Args:
            title: Title string to validate

        Returns:
            Tuple of (is_valid, error_message)
            - (True, None) if valid
            - (False, error_message) if invalid
        """
        if not title or not title.strip():
            return False, "Task title cannot be empty."

        if len(title) > self.MAX_TITLE_LENGTH:
            return False, f"Task title cannot exceed {self.MAX_TITLE_LENGTH} characters."

        return True, None

    def validate_description(self, description: Optional[str]) -> Tuple[bool, Optional[str]]:
        """Validate task description.

        Args:
            description: Description string to validate

        Returns:
            Tuple of (is_valid, error_message)
            - (True, None) if valid
            - (False, error_message) if invalid
        """
        # Description is optional, None is valid
        if description is None or not description.strip():
            return True, None

        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            return False, f"Task description cannot exceed {self.MAX_DESCRIPTION_LENGTH} characters."

        return True, None

    def validate_task_id(self, task_id_input: str) -> Tuple[bool, Optional[int], Optional[str]]:
        """Validate and parse task ID from user input.

        Args:
            task_id_input: Raw task ID input from user

        Returns:
            Tuple of (is_valid, parsed_id, error_message)
            - (True, id, None) if valid
            - (False, None, error_message) if invalid
        """
        if not task_id_input or not task_id_input.strip():
            return False, None, "Task ID is required."

        try:
            task_id = int(task_id_input.strip())
        except ValueError:
            return False, None, "Task ID must be a number."

        if task_id <= 0:
            return False, None, "Task ID must be a positive integer."

        return True, task_id, None

    def validate_menu_choice(self, choice: str, min_option: int, max_option: int) -> Tuple[bool, Optional[str]]:
        """Validate menu choice is within valid range.

        Args:
            choice: User's menu selection
            min_option: Minimum valid option number
            max_option: Maximum valid option number

        Returns:
            Tuple of (is_valid, error_message)
            - (True, None) if valid
            - (False, error_message) if invalid
        """
        if not choice or not choice.strip():
            return False, "Please select an option."

        if not choice.isdigit():
            return False, "Please enter a valid number."

        choice_num = int(choice)
        if choice_num < min_option or choice_num > max_option:
            return False, f"Invalid option. Please select {min_option}-{max_option}."

        return True, None

    def validate_confirmation(self, confirmation: str) -> bool:
        """Validate yes/no confirmation input.

        Args:
            confirmation: User's confirmation input

        Returns:
            True if user confirmed (y/yes), False otherwise
        """
        return confirmation.strip().lower() in ("y", "yes")

    def clean_input(self, user_input: Optional[str]) -> Optional[str]:
        """Clean user input by stripping whitespace.

        Args:
            user_input: Raw user input

        Returns:
            Cleaned string or None if empty
        """
        if not user_input or not user_input.strip():
            return None
        return user_input.strip()
