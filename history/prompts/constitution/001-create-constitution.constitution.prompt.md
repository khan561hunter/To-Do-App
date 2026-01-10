---
id: 001
title: Create constitution
stage: constitution
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-todo-app-core
user: unknown
command: /sp.constitution
labels: [constitution, setup, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-create-constitution.constitution.prompt.md
tests:
  - none
---

## Prompt

# 📜 CONSTITUTION
## Phase I: In-Memory Python Console Todo Application

---

## 1. Purpose & Authority

This Constitution governs the development of **Phase I: Todo In-Memory Python Console App** using **Claude Code** and **Spec-Kit Plus**.

All development **must strictly follow** an **agentic, spec-driven workflow**.
Any deviation from this constitution is considered a failure of the project phase.

Claude Code acts as the **sole implementation agent**.
**No manual coding, refactoring, or file editing by humans is permitted.**

---

## 2. Project Objective

The objective is to build a **command-line Todo application** that:

- Runs entirely in the console
- Stores all data **in memory only**
- Loses all data upon program termination
- Demonstrates clean architecture, readable code, and logical correctness

This phase focuses on **logic, structure, and correctness**, not persistence or UI frameworks.

---

## 3. Scope Definition

### 3.1 In-Memory Constraint (Mandatory)

- All application state **must exist only in RAM**
- No files, databases, caches, or external storage
- Python data structures (lists, dictionaries, objects) only

If the program exits, **all tasks must be lost**.

---

## 4. Required Features (Basic Level – Mandatory)

The application **must implement all five features** listed below:

### 4.1 Add Task
- Title (required)
- Description (optional)
- Auto-generated unique ID
- Default status: incomplete

### 4.2 View Tasks
- Display all tasks
- Show ID, title, description, and status
- Clear visual indicator for completed vs incomplete

### 4.3 Update Task
- Update title and/or description
- Target task by ID
- Graceful handling of invalid IDs

### 4.4 Delete Task
- Delete task by ID
- Confirm deletion action

### 4.5 Mark Task Complete / Incomplete
- Toggle completion state
- Reflect status immediately in task listing

---

## 5. Development Methodology (Agentic Dev Stack)

Development **must strictly follow this sequence**.

### 5.1 Phase Order (Non-Negotiable)

1. **Write Specification**
   - Use Spec-Kit Plus format
   - Define behavior, constraints, and acceptance criteria
   - Save all specs in `/specs-history/`

2. **Generate Implementation Plan**
   - High-level architecture
   - Module responsibilities
   - Data structures

3. **Break Plan into Tasks**
   - Discrete, verifiable implementation steps
   - Each task must map back to the specification

4. **Implementation via Claude Code**
   - Claude generates all source files
   - No human edits
   - Clean, readable, Pythonic code

Claude **must not skip, merge, or reorder phases**.

---

## 6. Clean Code & Architecture Rules

Claude Code must enforce:

- Clear separation of concerns
- No duplicated logic
- Meaningful variable and function names
- Small, testable functions
- Predictable control flow

---

## 7. Technology Stack (Locked)

Claude Code must use **only** the following:

- Python **3.13+**
- UV (environment & dependency management)
- Claude Code
- Spec-Kit Plus

❌ No databases
❌ No ORMs
❌ No UI frameworks
❌ No external APIs

---

## 8. Deliverables (Required)

The GitHub repository **must contain**:

1. `CONSTITUTION.md`
   - This document

2. `/specs-history/`
   - All specification files
   - No deleted or overwritten specs

3. `/src/`
   - Complete Python source code
   - Runnable console application

4. `README.md`
   - Project overview
   - Setup instructions
   - How to run the app

5. `CLAUDE.md`
   - Instructions for Claude Code
   - Spec processing rules
   - Workflow and constraints

---

## 9. Platform Constraint (Windows Users)

Windows users **must use WSL 2**.

### Required Setup

```bash
# Install WSL 2
wsl --install

# Set WSL 2 as default
wsl --set-default-version 2

# Install Ubuntu
wsl --install -d Ubuntu-22.04
```

## Response snapshot

Created constitution file at `.specify/memory/constitution.md` with complete governance document defining:
- Project objective for in-memory Python console Todo application
- In-memory constraint (RAM-only, no persistence)
- Five required features: Add Task, View Tasks, Update Task, Delete Task, Mark Complete/Incomplete
- Mandatory development methodology with non-negotiable phase order (Spec → Plan → Tasks → Implementation)
- Clean code and architecture rules
- Locked technology stack: Python 3.13+, UV, Claude Code, Spec-Kit Plus
- Required deliverables including CONSTITUTION.md, specs-history/, src/, README.md, CLAUDE.md
- Platform constraint requiring WSL 2 for Windows users

Template consistency verified with spec/plan/tasks templates (no placeholders, alignment confirmed).

## Outcome

- ✅ Impact: Created new project constitution establishing governance for Phase I Todo app
- 🧪 Tests: none
- 📁 Files: Created `.specify/memory/constitution.md`, PHR record
- 🔁 Next prompts: Continue with `/sp.specify` to create feature specification
- 🧠 Reflection: Constitution provides clear, non-negotiable rules. User input was complete with no placeholder tokens, requiring direct write without substitution.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): initial
- Next experiment (smallest change to try): none
