# Agent-Based Architecture - Todo Console App

## Overview
This document explains the reusable agent-based architecture implemented in the Todo console application.

## Architecture Principles
1. **Single Responsibility**: Each agent has one clear purpose
2. **No Global State**: Agents communicate via method calls
3. **Dependency Injection**: Agents receive dependencies through constructors
4. **Reusability**: Each agent can be used in other console projects

---

## Agent Structure

### Project File Structure
```
src/
├── agents/                      # All reusable agents
│   ├── __init__.py             # Package exports
│   ├── todo_app_agent.py       # Main controller agent
│   ├── command_router_agent.py # Command routing
│   ├── task_agent.py           # Task business logic
│   ├── storage_agent.py        # In-memory storage
│   ├── validation_agent.py     # Input validation
│   └── display_agent.py        # Console output
├── todo_app/                    # Original models
│   ├── models.py               # Task model
│   └── ...
└── main_agent.py               # New entry point
```

---

## Agent Descriptions

### 1. TodoAppAgent (Main Controller)
**File**: `agents/todo_app_agent.py`

**Responsibility**: Orchestrate the application flow

**Does**:
- Initialize all sub-agents
- Run the main application loop
- Handle keyboard interrupts (Ctrl+C)
- Coordinate between sub-agents

**Does NOT**:
- Handle user input directly
- Display anything to console
- Perform business logic
- Access storage

**Key Methods**:
```python
start()                    # Start the application
_get_validated_choice()    # Get validated menu choice
```

---

### 2. CommandRouterAgent
**File**: `agents/command_router_agent.py`

**Responsibility**: Route commands to appropriate handlers

**Does**:
- Map menu choices to handler methods
- Coordinate between display, validation, and task agents
- Collect user input via display agent
- Call task agent for operations

**Does NOT**:
- Perform validation logic
- Display output directly
- Access storage directly
- Perform business logic

**Key Methods**:
```python
route_command(choice)      # Route to appropriate handler
_handle_add_task()         # Handle add operation
_handle_view_tasks()       # Handle view operation
_handle_update_task()      # Handle update operation
_handle_delete_task()      # Handle delete operation
_handle_toggle_complete()  # Handle toggle operation
```

---

### 3. TaskAgent
**File**: `agents/task_agent.py`

**Responsibility**: Manage task operations and business rules

**Does**:
- Create new tasks
- Update existing tasks
- Delete tasks
- Toggle task completion
- Enforce business rules

**Does NOT**:
- Handle storage directly (delegates to StorageAgent)
- Validate input (delegates to ValidationAgent)
- Display output
- Collect user input

**Key Methods**:
```python
create_task(title, description)           # Create new task
get_all_tasks()                            # Get all tasks
get_task(task_id)                          # Get specific task
update_task(task_id, title, description)   # Update task
delete_task(task_id)                       # Delete task
toggle_completion(task_id)                 # Toggle completion
```

**Return Format**:
All methods return tuples: `(success, result, error_message)`

---

### 4. StorageAgent
**File**: `agents/storage_agent.py`

**Responsibility**: Manage in-memory task storage

**Does**:
- Maintain task list in memory
- Provide CRUD storage operations
- Generate unique IDs
- Check task existence

**Does NOT**:
- Validate data
- Perform business logic
- Display anything
- Handle user input

**Key Methods**:
```python
save(task)          # Save task to storage
get_all()           # Get all tasks
get_by_id(task_id)  # Get task by ID
remove(task)        # Remove task from storage
generate_id()       # Generate unique ID
exists(task_id)     # Check if task exists
```

**Reusability**: Can be replaced with file or database storage agent

---

### 5. ValidationAgent
**File**: `agents/validation_agent.py`

**Responsibility**: Validate all user inputs

**Does**:
- Validate task titles (non-empty, length limits)
- Validate descriptions (length limits)
- Validate task IDs (numeric, positive)
- Validate menu choices (range checking)
- Validate confirmations (yes/no)
- Clean user input (strip whitespace)

**Does NOT**:
- Perform operations
- Access storage
- Display messages
- Collect input

**Key Methods**:
```python
validate_title(title)                          # Validate title
validate_description(description)              # Validate description
validate_task_id(task_id_input)                # Parse and validate ID
validate_menu_choice(choice, min, max)         # Validate menu choice
validate_confirmation(confirmation)            # Validate yes/no
clean_input(user_input)                        # Clean input string
```

**Return Format**:
- `(is_valid, error_message)` or
- `(is_valid, parsed_value, error_message)`

**Configuration**:
```python
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 500
```

---

### 6. DisplayAgent
**File**: `agents/display_agent.py`

**Responsibility**: Handle all console output

**Does**:
- Display main menu
- Show section headers
- Format and display tasks
- Show success messages
- Show error messages
- Show info messages
- Prompt for user input
- Display exit message

**Does NOT**:
- Perform validation
- Perform operations
- Access storage
- Contain business logic

**Key Methods**:
```python
show_menu()                # Display main menu
show_header(title)         # Display section header
show_tasks(tasks)          # Display task list
show_success(message)      # Display success message
show_error(message)        # Display error message
show_info(message)         # Display info message
prompt_input(prompt_text)  # Get user input
show_exit_message()        # Display exit message
```

---

## Agent Interaction Flow

### Example: User Adds a Task

```
1. User runs application
   └─> TodoAppAgent.start()

2. Main loop displays menu
   └─> DisplayAgent.show_menu()

3. User enters "1" (Add Task)
   └─> TodoAppAgent._get_validated_choice()
       └─> DisplayAgent.prompt_input()
       └─> ValidationAgent.validate_menu_choice()

4. Command routed to handler
   └─> CommandRouterAgent.route_command("1")
       └─> CommandRouterAgent._handle_add_task()

5. Get task details from user
   └─> DisplayAgent.show_header("Add Task")
   └─> DisplayAgent.prompt_input("Enter task title: ")
   └─> DisplayAgent.prompt_input("Enter description: ")

6. Create task
   └─> TaskAgent.create_task(title, description)
       ├─> ValidationAgent.validate_title(title)
       ├─> ValidationAgent.validate_description(description)
       ├─> ValidationAgent.clean_input(title)
       ├─> StorageAgent.generate_id()
       └─> StorageAgent.save(task)

7. Display result
   └─> DisplayAgent.show_success("Task created with ID: 1")

8. Loop back to step 2
```

---

## How Agents Are Reused

### StorageAgent
Can be used in ANY project needing in-memory storage:
- Note-taking app
- Contact manager
- Inventory system
- Any CRUD application

**To replace with file storage**:
1. Create `FileStorageAgent` with same methods
2. Update `TodoAppAgent.__init__()` to use new agent
3. No changes needed in other agents

### ValidationAgent
Can be used in ANY project needing input validation:
- Form validation
- Configuration validation
- API input validation
- Command-line argument validation

**Customizable**:
- Change `MAX_TITLE_LENGTH` and `MAX_DESCRIPTION_LENGTH`
- Add new validation methods
- Reuse existing validation methods

### DisplayAgent
Can be used in ANY console application:
- Menu-driven apps
- CLI tools
- Interactive scripts
- Console games

**Customizable**:
- Modify menu format
- Add colors (with libraries)
- Add more formatting methods
- Change message styles

### TaskAgent
Can be adapted for ANY entity management:
- User management
- Product management
- Order management
- Any business entity

**To adapt**:
1. Replace `Task` with your entity
2. Adjust methods for your operations
3. Keep same delegation pattern

### CommandRouterAgent
Can be used in ANY menu-driven console app:
- Database admin tools
- System utilities
- File managers
- Any interactive CLI

**To adapt**:
1. Change menu options
2. Update handler methods
3. Keep same routing pattern

---

## Benefits of This Architecture

### 1. Testability
Each agent can be tested independently:
```python
# Test StorageAgent alone
storage = StorageAgent()
task_id = storage.generate_id()
assert task_id == 1

# Test ValidationAgent alone
validator = ValidationAgent()
is_valid, error = validator.validate_title("")
assert not is_valid
assert error == "Task title cannot be empty."
```

### 2. Maintainability
Changes are isolated to specific agents:
- Change validation rules → only modify ValidationAgent
- Change display format → only modify DisplayAgent
- Change storage → only modify StorageAgent

### 3. Reusability
Each agent can be copied to a new project:
- Copy `DisplayAgent` → use in any console app
- Copy `ValidationAgent` → use in any input validation
- Copy `StorageAgent` → use in any in-memory app

### 4. Readability
Clear separation of concerns:
- Each file has one purpose
- No mixing of display/logic/storage
- Easy to understand agent responsibilities

### 5. Extensibility
Easy to add new features:
- Add search → create `SearchAgent`
- Add filtering → extend `TaskAgent`
- Add persistence → replace `StorageAgent`

---

## Running the Application

### Using Agent Architecture
```bash
cd src
python main_agent.py
```

### Using Original Architecture
```bash
cd src
python main.py
```

Both versions provide the same functionality but with different architectures.

---

## Migration from Monolithic to Agent-Based

### Before (Monolithic)
```
main.py → TodoCLI (handles everything)
          ├─ Display logic
          ├─ Input validation
          ├─ Business logic
          └─ Calls TaskService
                    └─ Storage + Business logic
```

### After (Agent-Based)
```
main_agent.py → TodoAppAgent (orchestrates only)
                ├─> CommandRouterAgent (routes commands)
                │   ├─> TaskAgent (business logic)
                │   │   ├─> StorageAgent (storage)
                │   │   └─> ValidationAgent (validation)
                │   └─> DisplayAgent (output)
                ├─> ValidationAgent (input validation)
                └─> DisplayAgent (menu display)
```

---

## Code Examples

### Example 1: Create a Storage Agent Instance
```python
from agents import StorageAgent

storage = StorageAgent()
task_id = storage.generate_id()  # Returns 1
task_id = storage.generate_id()  # Returns 2
```

### Example 2: Validate Input
```python
from agents import ValidationAgent

validator = ValidationAgent()

# Validate title
is_valid, error = validator.validate_title("Buy milk")
# Returns: (True, None)

is_valid, error = validator.validate_title("")
# Returns: (False, "Task title cannot be empty.")

# Validate ID
is_valid, task_id, error = validator.validate_task_id("5")
# Returns: (True, 5, None)

is_valid, task_id, error = validator.validate_task_id("abc")
# Returns: (False, None, "Task ID must be a number.")
```

### Example 3: Display Output
```python
from agents import DisplayAgent

display = DisplayAgent()
display.show_menu()
# Prints formatted menu

display.show_success("Task created!")
# Prints: Task created!

display.show_error("Task not found.")
# Prints: Error: Task not found.
```

### Example 4: Create Task
```python
from agents import StorageAgent, ValidationAgent, TaskAgent

storage = StorageAgent()
validator = ValidationAgent()
task_agent = TaskAgent(storage, validator)

# Create task
success, task, error = task_agent.create_task("Buy milk", "From store")

if success:
    print(f"Created task with ID: {task.id}")
else:
    print(f"Error: {error}")
```

### Example 5: Full Application
```python
from agents import TodoAppAgent

# Create and start main agent
app = TodoAppAgent()
app.start()

# That's it! Main agent handles everything by delegating to sub-agents
```

---

## Beginner-Friendly Design

### Clear Comments
Every file has:
- Purpose explanation at the top
- Responsibility description
- What it DOES
- What it DOES NOT do

### Descriptive Names
- `StorageAgent` → clearly manages storage
- `ValidationAgent` → clearly handles validation
- `DisplayAgent` → clearly handles display
- `TaskAgent` → clearly manages tasks

### Simple Methods
Each method:
- Has a single purpose
- Returns clear results
- Has clear parameter names
- Includes docstrings

### No Complex Patterns
- No decorators
- No metaclasses
- No complex inheritance
- Just simple classes and methods

---

## Next Steps

### To Extend This Application
1. Add filtering → Create `FilterAgent`
2. Add search → Create `SearchAgent`
3. Add sorting → Extend `TaskAgent` with sort methods
4. Add categories → Extend `Task` model and agents
5. Add file persistence → Replace `StorageAgent` with `FileStorageAgent`

### To Use in Another Project
1. Copy relevant agent files
2. Replace `Task` with your entity
3. Adjust validation rules
4. Update display messages
5. Create your main agent

---

## Summary

This agent-based architecture provides:
- **Separation of concerns**: Each agent has one job
- **Reusability**: Agents can be used in other projects
- **Maintainability**: Changes are isolated
- **Testability**: Each agent can be tested independently
- **Clarity**: Clear responsibilities and interactions

Each agent is self-contained, well-documented, and designed to be understood and reused by beginners.
