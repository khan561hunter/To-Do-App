---
id: 003
title: Generate full-stack tasks
stage: tasks
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-fullstack-web-app
branch: 002-fullstack-web-app
user: hp
command: /sp.tasks
labels: ["tasks","fullstack","fastapi","nextjs","docker"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-fullstack-web-app/tasks.md
tests:
 - (not run)
---

## Prompt

<command-message>sp.tasks</command-message>
<command-name>/sp.tasks</command-name>
<command-args>[Pasted text #1 +300 lines]</command-args>## User Input

```text
[Pasted text #1 +300 lines]
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: [Pasted text #1 +300 lines]

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent-native tools when possible.

## Response snapshot

- Generated `specs/002-fullstack-web-app/tasks.md` using plan.md, spec.md, data-model.md, contracts/api-spec.yaml, research.md, and quickstart.md.
- Organized tasks into Phase 1 Setup, Phase 2 Foundational, then user story phases in priority order (US1, US2, US4, US3), followed by Docker/E2E polish.
- Validated tasks checklist format and sequential numbering (T001–T062) and added parallel examples.

## Outcome

- ✅ Impact: Feature now has an executable, dependency-ordered implementation task list aligned to the approved plan/spec.
- 🧪 Tests: Not run (task generation only).
- 📁 Files: Created specs/002-fullstack-web-app/tasks.md.
- 🔁 Next prompts: Run /sp.implement to start execution, or request changes to task ordering/scope.
- 🧠 Reflection: Ensure task lines remain strict checklist format; keep examples from being interpreted as tasks.

## Evaluation notes (flywheel)

- Failure modes observed: PHR shell script unavailable on Windows; created PHR via template fallback.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add a Windows-compatible PHR creation script or update docs to prefer agent-native template flow on Windows.
