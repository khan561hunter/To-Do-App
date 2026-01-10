---

description: "Task list template for feature implementation"
---

# Tasks: In-Memory Python Console Todo Application

**Input**: Design documents from `/specs/001-todo-console/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The spec does not require tests, so no test tasks are included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow project structure from plan.md

<!--
  ============================================================================
  No sample tasks - this is directly generated based on spec, plan, and design docs.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan (src/, src/todo_app/, with __init__.py, models.py, services.py, cli.py)
- [X] T002 Initialize Python project with UV (pyproject.toml or requirements.txt)
- [X] T003 [P] Configure Python 3.13+ in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Implement Task model in src/todo_app/models.py with id, title, description, completed fields
- [X] T005 Implement TaskService class in src/todo_app/services.py with _tasks list and _next_id counter
- [X] T006 [P] Implement add_task method in TaskService (returns Task with auto-generated ID)
- [X] T007 [P] Implement get_all_tasks method in TaskService (returns List[Task])
- [X] T008 [P] Implement get_task_by_id method in TaskService (returns Optional[Task])
- [X] T009 [P] Implement update_task method in TaskService (selective updates, raises ValueError)
- [X] T010 [P] Implement delete_task method in TaskService (raises ValueError if ID invalid)
- [X] T011 [P] Implement toggle_complete method in TaskService (inverts completed status)
- [X] T012 Configure error handling with ValueError messages per service contract
- [X] T013 Create empty __init__.py in src/todo_app/ for package initialization

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Allow users to create new tasks and view all tasks in the list.

**Independent Test**: Can be fully tested by creating tasks, viewing the list, and verifying tasks appear with ID, title, description, and status.

### Implementation for User Story 1

- [X] T014 [US1] Create menu display function in src/todo_app/cli.py showing options 1-6
- [X] T015 [US1] Implement menu input loop in src/todo_app/cli.py with validation (1-6)
- [X] T016 [US1] Implement "Add Task" option handler in src/todo_app/cli.py (prompts for title and description)
- [X] T017 [US1] Implement "View Tasks" option handler in src/todo_app/cli.py (displays all tasks with visual indicators)
- [X] T018 [US1] Implement empty state message in src/todo_app/cli.py when no tasks exist
- [X] T019 [US1] Implement visual indicator for completed vs incomplete tasks in src/todo_app/cli.py (e.g., [✓] Complete vs [ ] Incomplete)
- [X] T020 [US1] Add title validation in src/todo_app/cli.py (non-empty check before calling service)
- [X] T021 [US1] Connect "Add Task" CLI handler to TaskService.add_task in src/todo_app/cli.py
- [X] T022 [US1] Connect "View Tasks" CLI handler to TaskService.get_all_tasks in src/todo_app/cli.py

**Checkpoint**: At this point, User Story 1 (Create and View Tasks) should be fully functional and independently testable as MVP

---

## Phase 4: User Story 2 - Update and Complete Tasks (Priority: P2)

**Goal**: Allow users to update task details and toggle completion status.

**Independent Test**: Can be tested by updating existing task titles/descriptions and toggling completion status, then viewing updated task list.

### Implementation for User Story 2

- [X] T023 [US2] Implement "Update Task" option handler in src/todo_app/cli.py (prompts for task ID, title, description)
- [X] T024 [US2] Implement "Mark Complete/Incomplete" option handler in src/todo_app/cli.py (prompts for task ID)
- [X] T025 [US2] Implement selective update logic in src/todo_app/cli.py (only update non-None fields)
- [X] T026 [US2] Add task ID validation in src/todo_app/cli.py for update/complete operations
- [X] T027 [US2] Connect "Update Task" CLI handler to TaskService.update_task in src/todo_app/cli.py
- [X] T028 [US2] Connect "Mark Complete/Incomplete" CLI handler to TaskService.toggle_complete in src/todo_app/cli.py
- [X] T029 [US2] Implement success message display in src/todo_app/cli.py after update/complete operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Delete Tasks (Priority: P3)

**Goal**: Allow users to delete tasks with confirmation.

**Independent Test**: Can be tested by creating tasks, deleting them, and verifying they no longer appear in task list.

### Implementation for User Story 3

- [X] T030 [US3] Implement "Delete Task" option handler in src/todo_app/cli.py (prompts for task ID)
- [X] T031 [US3] Implement confirmation prompt in src/todo_app/cli.py (y/n or yes/no)
- [X] T032 [US3] Add task ID validation for delete operation in src/todo_app/cli.py
- [X] T033 [US3] Connect "Delete Task" CLI handler to TaskService.delete_task in src/todo_app/cli.py
- [X] T034 [US3] Implement confirmation message display in src/todo_app/cli.py after successful deletion

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T035 [P] Implement global error handler in src/todo_app/cli.py for ValueError from TaskService
- [X] T036 [P] Implement invalid menu selection handling in src/todo_app/cli.py ("Invalid option. Please select 1-6.")
- [X] T037 [P] Implement KeyboardInterrupt handler in src/todo_app/cli.py for graceful Ctrl+C exit
- [X] T038 [P] Implement "Exit" option handler in src/todo_app/cli.py (ends main loop with message)
- [X] T039 [P] Implement human-readable error messages for all error types in src/todo_app/cli.py
- [X] T040 Create main entry point in src/main.py (initializes TaskService and CLI, starts main loop)
- [X] T041 [P] Ensure main.py activates todo_app package (import CLI, create service instance)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3)
  - US2 tasks depend on US1 foundation (shared CLI structure)
  - US3 tasks depend on US1 foundation (shared CLI structure)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for CLI framework patterns
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 for CLI framework patterns

### Within Each User Story

- Models before services
- Services before CLI handlers
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003)
- All Foundational tasks marked [P] can run in parallel (T006, T007, T008, T009, T010, T011, T012)
- Once Foundational phase completes, user stories must proceed sequentially (US1 → US2 → US3) due to shared CLI framework
- All Polish phase tasks marked [P] can run in parallel (T035, T036, T037, T040, T041)

---

## Parallel Example: Foundational Phase

```bash
# Launch all service methods together:
Task: "Implement add_task method in TaskService (returns Task with auto-generated ID)"
Task: "Implement get_all_tasks method in TaskService (returns List[Task])"
Task: "Implement get_task_by_id method in TaskService (returns Optional[Task])"
Task: "Implement update_task method in TaskService (selective updates, raises ValueError)"
Task: "Implement delete_task method in TaskService (raises ValueError if ID invalid)"
Task: "Implement toggle_complete method in TaskService (inverts completed status)"
```

---

## Parallel Example: Polish Phase

```bash
# Launch all polish tasks together:
Task: "Implement global error handler in src/todo_app/cli.py for ValueError from TaskService"
Task: "Implement invalid menu selection handling in src/todo_app/cli.py"
Task: "Implement KeyboardInterrupt handler in src/todo_app/cli.py for graceful Ctrl+C exit"
Task: "Implement 'Exit' option handler in src/todo_app/cli.py (ends main loop with message)"
Task: "Ensure main.py activates todo_app package (import CLI, create service instance)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Create and View Tasks)
4. **STOP and VALIDATE**: Test User Story 1 independently (create task, view task, verify empty state)
5. Run application and verify MVP delivers value

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP delivers value
3. Add User Story 2 → Test independently → Update and Complete features
4. Add User Story 3 → Test independently → Delete functionality
5. Add Polish Phase → Error handling, Exit, graceful termination
6. Each story adds value without breaking previous stories

### Sequential Story Execution

Due to shared CLI framework:

1. Team completes Setup + Foundational together
2. Implement User Story 1 fully (menu, add task, view task, empty state, validation)
3. Implement User Story 2 (update task, toggle complete, validation)
4. Implement User Story 3 (delete task, confirmation, validation)
5. Implement Polish (all error handlers, exit, main entry point)
6. Stories complete and integrate in sequence, using shared CLI patterns from US1

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Foundational phase (T004-T013) BLOCKS all user stories
- US1 (T014-T022) establishes CLI patterns used by US2 and US3
- T003 can run parallel with T002 (UV initialization and Python version config)
- No tests per spec - tasks focus on implementation only
- Verify in-memory constraint: data exists only in RAM, lost on exit (FR-012)
