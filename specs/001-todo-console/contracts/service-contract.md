# Service Layer Contract

**Feature**: In-Memory Python Console Todo Application
**Branch**: 001-todo-console
**Date**: 2025-12-27
**Version**: 1.0

---

## Overview

This document defines the contract for the **TaskService** layer. The service layer provides business logic and in-memory task storage, with a well-defined interface for the CLI layer to consume.

---

## Service Interface

### Class: TaskService

**Responsibilities**:
- Maintain in-memory task collection
- Provide CRUD operations for tasks
- Enforce business rules and validations
- Manage auto-incrementing ID generation

---

## Methods

### add_task

**Signature**:
```python
def add_task(title: str, description: Optional[str]) -> Task
```

**Description**:
Creates a new task with auto-generated ID and adds it to the in-memory store.

**Parameters**:
- `title` (str, required): Task title. Must be non-empty after stripping whitespace.
- `description` (Optional[str], optional): Task details. Can be None or non-empty string.

**Returns**:
- `Task`: The newly created Task object with auto-generated ID

**Raises**:
- `ValueError`: If title is empty or whitespace-only

**Business Rules**:
1. Title must be non-empty after `strip()`
2. Title maximum 200 characters
3. Description maximum 500 characters
4. ID auto-generated starting from 1, incremented by 1 for each new task
5. Default `completed` status is `False`

**Example**:
```python
service = TaskService()
task = service.add_task("Buy groceries", "Milk, eggs, bread")
# Returns: Task(id=1, title="Buy groceries", description="Milk, eggs, bread", completed=False)
```

---

### get_all_tasks

**Signature**:
```python
def get_all_tasks() -> List[Task]
```

**Description**:
Returns all tasks currently stored in memory.

**Parameters**:
- None

**Returns**:
- `List[Task]`: List of all Task objects in insertion order

**Raises**:
- None

**Business Rules**:
1. Returns empty list if no tasks exist
2. Order: Insertion order (as created)

**Example**:
```python
service = TaskService()
tasks = service.get_all_tasks()
# Returns: [Task(id=1, ...), Task(id=2, ...)]
```

---

### get_task_by_id

**Signature**:
```python
def get_task_by_id(task_id: int) -> Optional[Task]
```

**Description**:
Retrieves a specific task by its ID.

**Parameters**:
- `task_id` (int, required): Unique task identifier

**Returns**:
- `Optional[Task]`: Task object if found, None if ID doesn't exist

**Raises**:
- `ValueError`: If task_id is not a positive integer

**Business Rules**:
1. Searches linearly through task list
2. Returns None if ID doesn't exist (doesn't raise error)

**Example**:
```python
service = TaskService()
task = service.get_task_by_id(1)
# Returns: Task(id=1, ...) or None
```

---

### update_task

**Signature**:
```python
def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task
```

**Description**:
Updates task title and/or description selectively. Only non-None parameters are updated.

**Parameters**:
- `task_id` (int, required): Unique task identifier
- `title` (Optional[str], optional): New title. If None, title unchanged.
- `description` (Optional[str], optional): New description. If None, description unchanged.

**Returns**:
- `Task`: The updated Task object

**Raises**:
- `ValueError`: If task_id not found, or if title/description invalid

**Business Rules**:
1. Task must exist with given task_id
2. If title provided and non-empty: update title
3. If title provided and empty: raise ValueError
4. If description provided (including None): update description
5. `completed` status is NOT modified by this method

**Example**:
```python
service = TaskService()
updated = service.update_task(1, title="New title")
# Updates only title, description and completed unchanged
```

---

### delete_task

**Signature**:
```python
def delete_task(task_id: int) -> None
```

**Description**:
Removes a task from the in-memory store permanently.

**Parameters**:
- `task_id` (int, required): Unique task identifier

**Returns**:
- None

**Raises**:
- `ValueError`: If task_id not found

**Business Rules**:
1. Task must exist with given task_id
2. Task is permanently removed from memory
3. IDs are not reused (deleted tasks leave gaps in sequence)

**Example**:
```python
service = TaskService()
service.delete_task(1)
# Task 1 removed from memory, ID 1 will not be reused
```

---

### toggle_complete

**Signature**:
```python
def toggle_complete(task_id: int) -> Task
```

**Description**:
Toggles the completion status of a task (False ↔ True).

**Parameters**:
- `task_id` (int, required): Unique task identifier

**Returns**:
- `Task`: The updated Task object with toggled status

**Raises**:
- `ValueError`: If task_id not found

**Business Rules**:
1. Task must exist with given task_id
2. Inverts current `completed` value
3. Returns updated Task object

**Example**:
```python
service = TaskService()
task = service.toggle_complete(1)
# If task.completed was False, now True (and vice versa)
```

---

## Error Handling

### ValueError

Raised by service methods when validation fails:

| Method              | Raises When                                      | Error Message Format                        |
|---------------------|---------------------------------------------------|---------------------------------------------|
| `add_task`          | Title is empty or whitespace-only                | "Task title cannot be empty."            |
| `get_task_by_id`     | task_id is not positive integer                | "Task ID must be a positive integer."        |
| `update_task`        | task_id not found                              | "Task with ID {task_id} not found."       |
| `update_task`        | Title is empty (when provided)               | "Task title cannot be empty."            |
| `delete_task`        | task_id not found                              | "Task with ID {task_id} not found."       |
| `toggle_complete`     | task_id not found                              | "Task with ID {task_id} not found."       |

---

## Invariants

The TaskService guarantees these invariants at all times:

1. **ID Uniqueness**: No two tasks have the same ID
2. **Insertion Order**: `get_all_tasks()` returns tasks in creation order
3. **Non-Empty Title**: No task has empty or whitespace-only title
4. **ID Monotonicity**: IDs always increase (never decrease or reuse)

---

## State Diagram

```
TaskService Lifecycle:

[Initialize] → [_tasks=[], _next_id=1]
       ↓
[add_task] → [Task created with ID, appended to list, _next_id++]
       ↓
[update_task] → [Task found, fields updated in-place]
       ↓
[toggle_complete] → [Task found, completed flipped]
       ↓
[delete_task] → [Task found, removed from list, ID not reused]
       ↓
[get_all_tasks] → [Return all tasks in insertion order]
```

---

## Testing Contract

For manual testing of service contract:

```python
# Test 1: Add and retrieve
service = TaskService()
task = service.add_task("Test task", "Test description")
assert task.id == 1
assert task.title == "Test task"
assert task.completed == False

# Test 2: Update task
updated = service.update_task(1, title="Updated")
assert updated.title == "Updated"
assert updated.description == "Test description"  # Unchanged

# Test 3: Toggle complete
toggled = service.toggle_complete(1)
assert toggled.completed == True

# Test 4: Delete task
service.delete_task(1)
assert service.get_task_by_id(1) is None
```

---

## Version History

- **1.0** (2025-12-27): Initial contract definition
