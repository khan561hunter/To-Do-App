# Quickstart: In-Memory Python Console Todo Application

**Feature**: 001-todo-console
**Branch**: 001-todo-console
**Date**: 2025-12-27

---

## Overview

This quickstart guide provides minimal steps to run the In-Memory Python Console Todo Application after implementation is complete.

---

## Prerequisites

### Required

- Python 3.13 or higher
- UV (Python package manager)
- Terminal or console access

### Platform-Specific

**Windows Users**:
```bash
# Ensure WSL 2 is installed and active
wsl --list --verbose

# If not installed, run:
wsl --install -d Ubuntu-22.04
```

**Linux Users**:
- Native terminal access (no additional setup required)

---

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Check Out Feature Branch

```bash
git checkout 001-todo-console
```

### 3. Install UV (if not installed)

```bash
# On Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (via WSL 2)
# Same as Linux command above
```

### 4. Setup Python Environment

```bash
# Create virtual environment with UV
uv venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows (non-WSL)

# Install dependencies (if any added in future)
uv pip install -e .
```

---

## Running the Application

### Start the Todo Application

```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/macOS

# Run the application
python src/main.py
```

### Expected Output

```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit
=========================
Select option (1-6):
```

---

## Basic Usage

### Adding a Task

1. Select option `1` from menu
2. Enter task title when prompted
3. Enter task description (optional, press Enter to skip)

```
Select option (1-6): 1
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread

Task created with ID: 1
```

### Viewing Tasks

1. Select option `2` from menu
2. See all tasks with IDs, titles, descriptions, and completion status

```
Select option (1-6): 2

Tasks:
[1] Buy groceries (Incomplete)
      Description: Milk, eggs, bread

[2] Write documentation (Complete)
      Description: Complete API docs
```

### Updating a Task

1. Select option `3` from menu
2. Enter task ID to update
3. Enter new title (press Enter to keep current)
4. Enter new description (press Enter to keep current)

```
Select option (1-6): 3
Enter task ID: 1
Enter new title (press Enter to keep current): Buy weekly groceries
Enter new description (optional): Milk, eggs, bread, butter

Task 1 updated successfully
```

### Marking Task Complete/Incomplete

1. Select option `5` from menu
2. Enter task ID to toggle completion status

```
Select option (1-6): 5
Enter task ID: 1

Task 1 marked as Complete
```

### Deleting a Task

1. Select option `4` from menu
2. Enter task ID to delete
3. Confirm deletion by entering `y` or `yes`

```
Select option (1-6): 4
Enter task ID: 1
Delete this task? (y/n): y

Task 1 deleted successfully
```

### Exiting the Application

1. Select option `6` from menu

```
Select option (1-6): 6
Exiting application.
```

---

## Important Notes

### In-Memory Constraint

**⚠️ All data is lost when the application exits.**

This is intentional behavior per the constitution's in-memory requirement.

To verify:
1. Create a task
2. Select option `6` to exit
3. Re-run the application (`python src/main.py`)
4. Select option `2` to view tasks
5. Confirm: No tasks are displayed (empty state message shown)

### Error Handling

The application handles common errors gracefully:

- **Invalid menu option**: "Invalid option. Please select 1-6."
- **Task not found**: "Task with ID {id} not found."
- **Empty title**: "Task title cannot be empty."
- **Keyboard interrupt (Ctrl+C)**: "\nExiting application."

### Input Validation

- Task titles cannot be empty or whitespace-only
- Task IDs must be positive integers
- Descriptions are optional (press Enter to skip)

---

## Troubleshooting

### UV Not Found

```bash
# Verify UV is installed
uv --version

# If not found, reinstall
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Python Version Error

```bash
# Check Python version
python --version

# If Python < 3.13, install newer version
# Follow: https://www.python.org/downloads/
```

### Module Not Found

```bash
# Ensure you're in the project root directory
cd <repository-directory>

# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/macOS

# Reinstall if needed
uv pip install -e .
```

---

## Verification Checklist

After running the application, verify these work:

- [ ] Application starts without errors
- [ ] Menu displays correctly (options 1-6)
- [ ] Can add a task with title and optional description
- [ ] Can view all tasks with all fields displayed
- [ ] Can update a task's title and/or description
- [ ] Can toggle task completion status (Complete ↔ Incomplete)
- [ ] Can delete a task with confirmation
- [ ] Application exits cleanly with option 6
- [ ] Tasks are lost after restart (in-memory constraint verified)

---

## Next Steps

After quickstart verification:

1. Review [data-model.md](data-model.md) for Task entity details
2. Review [service-contract.md](contracts/service-contract.md) for service interface
3. Review [research.md](research.md) for architectural decisions
4. Review [plan.md](plan.md) for implementation strategy
5. Run `/sp.tasks` to generate implementation tasks

---

## Support

For issues or questions:

1. Check this quickstart guide
2. Review [spec.md](spec.md) for feature requirements
3. Review constitution (.specify/memory/constitution.md) for constraints
4. Check error messages in console output

---

## Known Limitations

Per Phase I scope and constitution:

- No data persistence (all data lost on exit)
- No search or filter functionality
- No task priorities or deadlines
- No multi-user support
- No collaboration or sharing features

These limitations are intentional for Phase I focus on clean architecture and in-memory logic.
