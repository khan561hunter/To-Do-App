# Implementation Plan: In-Memory Python Console Todo Application

**Branch**: `001-todo-console` | **Date**: 2025-12-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-todo-console/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Phase I of In-Memory Python Console Todo Application: Build a command-line interface for managing todo tasks stored entirely in memory. The application will provide five core features (Add, View, Update, Delete, Toggle Complete) using a clean, layered architecture with CLI, Service, and Model layers. All data is lost on program termination as mandated by the constitution.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only)
**Storage**: N/A (in-memory only)
**Testing**: N/A (no tests requested in spec)
**Target Platform**: Console/Terminal (Linux native, Windows via WSL 2)
**Project Type**: single
**Performance Goals**: <1s response time for all operations
**Constraints**: In-memory only, no persistence, no external APIs, <50MB memory footprint
**Scale/Scope**: 5 features, single-user, ~300 LOC expected

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **In-Memory Constraint**: All data stored in RAM, lost on termination (FR-012, SC-005)
- ✅ **Python 3.13+**: Specified in Technical Context
- ✅ **No Databases/ORMs/External APIs**: Storage marked N/A, primary dependencies set to None
- ✅ **Spec-Driven Workflow**: Follows constitution phases (Spec → Plan → Tasks → Implementation)
- ✅ **Clean Code**: Layered architecture planned with clear separation of concerns
- ✅ **UV Dependency Management**: Will be used for environment setup
- ✅ **Agentic Implementation**: Claude Code as sole implementation agent
- ✅ **Deliverables**: src/, README.md, CLAUDE.md planned

All gates PASS. Proceeding to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py
├── todo_app/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   └── cli.py
```

**Structure Decision**: Single project structure with clear module separation. `main.py` is entry point, `todo_app/` package contains business logic, `models.py` defines data structures, `services.py` manages in-memory state and operations, `cli.py` handles all user interaction. This structure enforces separation of concerns while keeping the codebase simple and maintainable.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations to track. All gates passed.

---

## Phase 0: Research & Decisions

### Architecture Approach

**Decision**: Layered architecture (CLI → Service → Model)

**Rationale**:
- Enforces clear separation of concerns per constitution Section 6
- CLI logic separated from business logic (constitution Section 10, FR requirement)
- Testable components with well-defined interfaces
- Predictable control flow and maintainability (constitution Section 11)

**Alternatives Considered**:
- Monolithic single-file: Rejected for poor separation of concerns
- MVC pattern: Overkill for simple console application
- Repository pattern: Unnecessary for in-memory store

### Data Structure Choice

**Decision**: Python list with Task objects for in-memory storage

**Rationale**:
- Simple and idiomatic for Python
- O(1) append, O(n) search/delete acceptable for small task counts
- Objects encapsulate task attributes clearly
- No external dependencies required

**Alternatives Considered**:
- Dictionary with ID keys: Slightly faster lookups but loses ordering
- Custom linked list: Over-engineering for this use case
- Database in memory: Violates "no databases" constraint

### ID Generation Strategy

**Decision**: Auto-incrementing integer starting from 1

**Rationale**:
- Unique within session guaranteed
- Simple to implement and understand
- User-friendly for console interface
- No external libraries needed

**Alternatives Considered**:
- UUID: Unnecessary complexity, harder for users to type
- Random integers: Requires collision detection
- String-based IDs: Harder to validate

---

## Phase 1: Data Model

### Task Entity

| Field        | Type    | Required | Description                     | Validation                          |
|-------------|----------|-----------|---------------------------------|-------------------------------------|
| id          | int      | Yes       | Auto-generated unique identifier    | Positive integer, unique            |
| title       | str      | Yes       | Short task title                  | Non-empty, trimmed whitespace      |
| description | str      | No        | Optional details                   | None or non-empty string          |
| completed   | bool     | Yes       | Completion status                  | Default: False                   |

### State Transitions

```
[New Task] → [Incomplete] (default)
[Incomplete] → [Complete] (toggle)
[Complete] → [Incomplete] (toggle)
```

### Validation Rules

1. Title cannot be empty after stripping whitespace
2. ID must exist in task store for update/delete/complete operations
3. ID must be positive integer
4. Description can be None or non-empty string (not empty string)

---

## Phase 1: Service Interface

### TaskService

**Responsibilities**:
- Maintain in-memory task collection
- Provide CRUD operations for tasks
- Enforce business rules and validations

**Operations**:

```python
class TaskService:
    def add_task(title: str, description: Optional[str]) -> Task
        """Create and store new task with auto-generated ID"""

    def get_all_tasks() -> List[Task]
        """Return all tasks in storage"""

    def get_task_by_id(task_id: int) -> Optional[Task]
        """Return task by ID or None if not found"""

    def update_task(task_id: int, title: Optional[str], description: Optional[str]) -> Task
        """Update task fields selectively, raises ValueError if ID invalid"""

    def delete_task(task_id: int) -> None
        """Remove task from storage, raises ValueError if ID invalid"""

    def toggle_complete(task_id: int) -> Task
        """Toggle completion status, raises ValueError if ID invalid"""
```

---

## Phase 1: CLI Interface

### CLI Menu Structure

```
=== Todo Application ====
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit
=========================
Select option (1-6):
```

### CLI Operations

- Display menu and prompt for input
- Validate menu selection (1-6)
- Delegate to TaskService
- Display success/error messages
- Loop until Exit selected

---

## Phase 1: Error Handling Strategy

### Error Types

1. **Invalid Menu Selection**: Display "Invalid option. Please select 1-6."
2. **Invalid Task ID**: Display "Task with ID {id} not found."
3. **Empty Task Title**: Display "Task title cannot be empty."
4. **KeyboardInterrupt**: Display "\nExiting application." and exit gracefully
5. **ValueError from Service**: Catch and display human-readable message

### Principles

- Never crash on recoverable errors
- Always provide actionable error messages
- Continue main loop after handling recoverable errors
- Exit only on explicit user action or unrecoverable errors

---

## Implementation Order

Per constitution Section 5.1 and plan Section 10:

1. Core data model (Task class in models.py)
2. In-memory task service (TaskService in services.py)
3. CLI menu framework (menu display and input loop in cli.py)
4. Add task functionality (CLI + service integration)
5. View task functionality (display formatting)
6. Update task functionality (ID validation, selective updates)
7. Delete task functionality (confirmation prompt)
8. Completion toggle functionality
9. Error handling and validation
10. Main entry point (main.py initialization)

---

## Validation Plan

After implementation, verify:

- ✅ All five features work correctly (Add, View, Update, Delete, Toggle Complete)
- ✅ Tasks are lost on program restart (create, exit, restart, verify empty)
- ✅ Application runs without uncaught exceptions
- ✅ Code follows layered architecture (no direct model access in CLI)
- ✅ All spec requirements satisfied (FR-001 through FR-012)
- ✅ Success criteria met (SC-001 through SC-005)

---

## Completion Criteria

This plan is considered complete when:

- All Phase 0 research decisions documented
- Phase 1 data model, service interface, and CLI structure defined
- Implementation order specified
- Validation plan created
- Constitution check passes
- Ready for `/sp.tasks` to generate implementation tasks
