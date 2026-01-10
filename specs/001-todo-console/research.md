# Research & Design Decisions

**Feature**: In-Memory Python Console Todo Application
**Branch**: 001-todo-console
**Date**: 2025-12-27

---

## Overview

This document consolidates research findings and architectural decisions for Phase I of the In-Memory Python Console Todo Application. All decisions align with the constitution's constraints (Section 3.1 in-memory requirement, Section 7 technology stack) and the feature specification.

---

## Architecture Decision

### Decision: Layered Architecture (CLI → Service → Model)

**Rationale**:
- Enforces clear separation of concerns as required by Constitution Section 6
- CLI layer handles user input/output, delegates to service layer
- Service layer contains business logic and manages task lifecycle
- Model layer defines data structures and enforces entity-level rules
- Testable components with well-defined interfaces
- Predictable control flow and maintainability (Constitution Section 11)

**Alternatives Considered**:

1. **Monolithic Single-File**
   - *Rejected*: Poor separation of concerns, violates Constitution Section 6
   - *Issue*: Business logic, UI, and data all mixed together

2. **MVC (Model-View-Controller) Pattern**
   - *Rejected*: Overkill for simple console application
   - *Issue*: Adds unnecessary complexity for read-only console display

3. **Repository Pattern**
   - *Rejected*: Unnecessary for in-memory store
   - *Issue*: Introduces abstraction layer without benefit when data never leaves memory

**Selected**: Layered architecture with CLI, Service, and Model layers

---

## Data Structure Decision

### Decision: Python List with Task Objects

**Rationale**:
- Simple and idiomatic for Python (standard library, no dependencies)
- O(1) append operations for task creation
- O(n) search/delete acceptable for small task counts (typical use: <100 tasks)
- Objects encapsulate task attributes clearly
- Maintains insertion order (important for task listing)
- No external libraries needed (aligns with Constitution Section 7)

**Alternatives Considered**:

1. **Dictionary with ID Keys**
   - *Rejected*: Loses ordering, complicates task listing
   - *Pros*: O(1) lookup by ID
   - *Cons*: Users expect tasks in creation order

2. **Custom Linked List**
   - *Rejected*: Over-engineering for this use case
   - *Issue*: Python list provides O(1) append and sufficient O(n) operations

3. **Database In Memory (SQLite, PostgreSQL)**
   - *Rejected*: Violates "no databases" constraint (Constitution Section 7)
   - *Issue*: Constitution explicitly prohibits all databases

**Selected**: Python list storing Task objects

---

## ID Generation Strategy

### Decision: Auto-Incrementing Integer Starting from 1

**Rationale**:
- Uniqueness guaranteed within session (no collisions)
- Simple to implement and understand
- User-friendly for console interface (easy to type)
- No external libraries or complex algorithms needed
- Follows natural user expectation (1, 2, 3... rather than random values)

**Alternatives Considered**:

1. **UUID (Universally Unique Identifier)**
   - *Rejected*: Unnecessary complexity, harder for users to type
   - *Pros*: Globally unique across sessions
   - *Cons*: Users struggle with typing UUIDs in console

2. **Random Integers**
   - *Rejected*: Requires collision detection logic
   - *Issue*: Adds complexity without benefit

3. **String-Based IDs**
   - *Rejected*: Harder to validate, longer to type
   - *Issue*: Users prefer numeric IDs for selection

**Selected**: Auto-incrementing integers starting at 1

---

## Console UI Approach

### Decision: Menu-Driven Interface with Numbered Options

**Rationale**:
- Standard pattern for console applications
- Clear, numbered options (1-6) easy to remember
- Reduces user input errors (discrete choices vs free-form)
- Simple to validate input
- Aligns with spec FR requirements and user stories

**Alternatives Considered**:

1. **Command-Line Arguments (Subcommands)**
   - *Rejected*: Requires users to remember command syntax
   - *Issue*: Less discoverable than menu for new users

2. **Text-Based Conversation Interface (Chatbot-style)**
   - *Rejected*: Over-engineering, violates simplicity principle
   - *Issue*: Complex NLP for simple CRUD operations

**Selected**: Menu-driven interface with numbered options (1-6)

---

## Error Handling Strategy

### Decision: Graceful Error Recovery with Human-Readable Messages

**Rationale**:
- Application must not crash on invalid input (Spec FR-010)
- All user errors must show human-readable messages (Spec Section 9)
- Continue main loop after recoverable errors
- Exit only on explicit user action or unrecoverable errors

**Error Types Handled**:

1. **Invalid Menu Selection**: Display "Invalid option. Please select 1-6."
2. **Invalid Task ID**: Display "Task with ID {id} not found."
3. **Empty Task Title**: Display "Task title cannot be empty."
4. **KeyboardInterrupt**: Display "\nExiting application." and exit gracefully
5. **ValueError from Service**: Catch and display human-readable message

**Alternatives Considered**:

1. **Silent Error Swallowing**
   - *Rejected*: Users confused when nothing happens
   - *Issue*: Spec FR-010 requires human-readable messages

2. **Stack Trace Display**
   - *Rejected*: Technical, intimidating for users
   - *Issue*: Violates "human-readable" requirement

**Selected**: Graceful error recovery with clear, actionable messages

---

## Technology Stack Confirmation

### Decision: Python 3.13+ Standard Library Only

**Rationale**:
- Mandated by Constitution Section 7
- No external dependencies needed for in-memory operations
- UV for environment management (as required by Constitution)
- Spec-compliant: no databases, ORMs, UI frameworks, or external APIs

**Confirmed Stack**:
- **Language**: Python 3.13+
- **Dependencies**: None (standard library only)
- **Environment Management**: UV
- **Storage**: In-memory Python list
- **Target Platform**: Console/Terminal (Linux native, Windows via WSL 2)

**Violations Checked**:
- ❌ No databases
- ❌ No ORMs
- ❌ No UI frameworks
- ❌ No external APIs
- ✅ In-memory only
- ✅ Python 3.13+
- ✅ UV for dependencies

---

## Summary

All architectural decisions align with:
1. **Constitution requirements**: In-memory constraint, technology stack, clean code principles
2. **Specification requirements**: All FRs and success criteria addressed
3. **Simplicity principle**: No over-engineering for a 5-feature console application
4. **User experience**: Clear menu interface, helpful error messages

No NEEDS CLARIFICATION items remain. Ready for Phase 1 data model and contract generation.
