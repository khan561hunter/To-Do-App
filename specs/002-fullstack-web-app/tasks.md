---

description: "Implementation task list for Full-Stack Web Application"
---

# Tasks: Full-Stack Web Application

**Input**: Design documents from `/specs/002-fullstack-web-app/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/api-spec.yaml, quickstart.md

**Tests**: Tests are OPTIONAL. The feature spec does not request TDD, so tasks below focus on implementation with **manual/independent verification steps** per user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and validation of each increment.

## Format (REQUIRED)

Every task line MUST follow:

```text
T### [P?] [US?] Description with file path
```

- `[P]` = parallelizable (different files, no dependency on incomplete tasks)
- `[US#]` story label ONLY for user story phases (no story labels in Setup/Foundational/Polish)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Validate repository structure and prepare the mandated monorepo layout.

- [X] T001 Validate required top-level directories exist: backend/, frontend/, specs/ (repo root)
- [X] T002 [P] Ensure Spec-Kit configuration is present under repo root .specify/: .specify/memory/constitution.md
- [X] T003 [P] Verify CLAUDE.md is discoverable at repo root: CLAUDE.md
- [X] T004 Create backend/ and frontend/ directories at repo root if missing: backend/, frontend/
- [X] T005 [P] Add backend/src/ package skeleton per plan.md: backend/src/__init__.py
- [X] T006 [P] Add frontend/src/ skeleton per plan.md: frontend/src/app/layout.tsx

**Checkpoint**: Monorepo layout exists and matches plan.md structure.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core backend/frontend foundations that MUST be complete before user stories.

### Backend foundation (FastAPI + config)

- [X] T007 Create backend Python project metadata per plan.md: backend/pyproject.toml
- [X] T008 Create backend dependency lock/requirements per plan.md: backend/requirements.txt
- [X] T009 Create backend app entrypoint FastAPI instance: backend/src/main.py
- [X] T010 Add environment loading and settings object (DATABASE_URL, JWT_SECRET, ports): backend/src/config.py
- [X] T011 Add database engine + session dependency (async SQLModel) wired to DATABASE_URL: backend/src/database.py
- [X] T012 [P] Create backend API package structure: backend/src/api/__init__.py
- [X] T013 [P] Create backend routes package structure: backend/src/api/routes/__init__.py
- [X] T014 Add /health endpoint per contracts/api-spec.yaml: backend/src/api/routes/health.py
- [X] T015 Wire routes into FastAPI app (include_router, tags, prefixes): backend/src/main.py

### Data models (SQLModel)

- [X] T016 [P] Implement SQLModel User table model per data-model.md: backend/src/models/user.py
- [X] T017 [P] Implement SQLModel Task table model per data-model.md: backend/src/models/task.py
- [X] T018 Add models package exports for imports: backend/src/models/__init__.py
- [X] T019 Add startup DB init (create_all) using SQLModel.metadata in app lifespan: backend/src/main.py

### Auth foundation (JWT verification middleware/dependency)

- [X] T020 Add auth middleware/dependency skeleton (HTTPBearer, token extraction): backend/src/middleware/auth_middleware.py
- [X] T021 Add JWT verify/claims decode using shared JWT_SECRET (401 on missing/invalid/expired): backend/src/services/auth_service.py
- [X] T022 Add FastAPI dependency get_current_user (loads User by id claim) for request context: backend/src/api/dependencies.py
- [X] T023 Ensure all /api/tasks* routes require auth dependency by default (security): backend/src/api/routes/tasks.py

**Checkpoint**: Backend boots, connects to Neon via DATABASE_URL, exposes /health, and has working JWT verification dependency.

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: User can register and log in, with a JWT usable for authenticated API calls.

**Independent Test** (manual):
- Register a user via `POST /api/auth/register`, then login via `POST /api/auth/login` and obtain a JWT.
- Call `GET /api/tasks` with `Authorization: Bearer <token>` and confirm it no longer returns 401.

### Implementation

- [X] T024 [P] [US1] Implement register route handler per contract (validate email/password; 409 on duplicate): backend/src/api/routes/auth.py
- [X] T025 [P] [US1] Implement login route handler per contract (401 on invalid credentials): backend/src/api/routes/auth.py
- [X] T026 [P] [US1] Add password hashing + verification utilities (bcrypt) used by auth routes: backend/src/services/auth_service.py
- [X] T027 [US1] Add auth router registration to the FastAPI app: backend/src/main.py

- [X] T028 [P] [US1] Initialize Next.js app router structure for auth pages per plan.md: frontend/src/app/(auth)/login/page.tsx
- [X] T029 [P] [US1] Add registration page UI posting to /api/auth/register: frontend/src/app/(auth)/register/page.tsx
- [X] T030 [P] [US1] Add Better Auth configuration scaffold and env wiring (JWT_SECRET): frontend/src/auth/better-auth.config.ts
- [X] T031 [US1] Implement session persistence strategy (store JWT from backend login in secure cookie via Better Auth or equivalent) and expose token getter for API client: frontend/src/auth/better-auth.config.ts
- [X] T032 [US1] Add protected dashboard layout redirecting unauthenticated users to /login: frontend/src/app/(dashboard)/layout.tsx

**Checkpoint**: User can register, login, and remains authenticated across reloads; protected routes redirect to login when unauthenticated.

---

## Phase 4: User Story 2 - Task CRUD Operations (Priority: P1)

**Goal**: Authenticated user can create/read/update/delete their tasks.

**Independent Test** (manual):
- With a valid JWT, create a task, list tasks, get task by id, update it, then delete it.

### Backend (CRUD endpoints)

- [X] T033 [P] [US2] Implement create task endpoint POST /api/tasks per contract (title required, defaults is_completed=false): backend/src/api/routes/tasks.py
- [X] T034 [P] [US2] Implement list tasks endpoint GET /api/tasks per contract (supports limit/offset/is_completed): backend/src/api/routes/tasks.py
- [X] T035 [P] [US2] Implement get task endpoint GET /api/tasks/{task_id} per contract: backend/src/api/routes/tasks.py
- [X] T036 [P] [US2] Implement update task endpoint PUT /api/tasks/{task_id} per contract: backend/src/api/routes/tasks.py
- [X] T037 [P] [US2] Implement delete task endpoint DELETE /api/tasks/{task_id} per contract: backend/src/api/routes/tasks.py

- [X] T038 [P] [US2] Add Task service methods (create/list/get/update/delete) using AsyncSession: backend/src/services/task_service.py
- [X] T039 [US2] Wire tasks routes to Task service methods and ensure DB session dependency injection: backend/src/api/routes/tasks.py

### Frontend (API client + UI)

- [X] T040 [P] [US2] Create centralized API client that attaches Authorization header from auth session: frontend/src/services/api.ts
- [X] T041 [P] [US2] Add typed task API wrappers (list/create/update/delete/get): frontend/src/services/tasks.ts
- [X] T042 [P] [US2] Build task dashboard page shell (server component) that renders task UI: frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T043 [P] [US2] Implement TaskList component (renders tasks, handles loading/errors): frontend/src/components/TaskList.tsx
- [X] T044 [P] [US2] Implement TaskForm component (create/edit task): frontend/src/components/TaskForm.tsx
- [X] T045 [P] [US2] Implement TaskItem component (edit/delete actions): frontend/src/components/TaskItem.tsx
- [X] T046 [US2] Connect dashboard page to API client (fetch, mutate, refresh UI state): frontend/src/app/(dashboard)/tasks/page.tsx

**Checkpoint**: CRUD works end-to-end for an authenticated user.

---

## Phase 5: User Story 4 - Multi-User Data Isolation (Priority: P1)

**Goal**: Each user can only access their own tasks; cross-user access is blocked.

**Independent Test** (manual):
- Create User A and User B.
- Create tasks as A; confirm B cannot list or fetch A's tasks.
- Attempt direct `GET /api/tasks/{task_id}` for A's task with B's token and confirm access is denied (403 or 404 per contract behavior).

### Implementation (backend enforcement)

- [X] T047 [US4] Ensure all Task service queries are filtered by authenticated user_id: backend/src/services/task_service.py
- [X] T048 [US4] Ensure get/update/delete endpoints enforce ownership (403 when task exists but not owned): backend/src/api/routes/tasks.py
- [X] T049 [US4] Ensure list endpoint only returns tasks for authenticated user (no cross-user leakage): backend/src/api/routes/tasks.py

### Implementation (frontend handling)

- [X] T050 [US4] Handle 401 responses globally by redirecting to /login and clearing session: frontend/src/services/api.ts

**Checkpoint**: Multi-user isolation holds for list/get/update/delete operations.

---

## Phase 6: User Story 3 - Task Completion Toggle (Priority: P2)

**Goal**: Authenticated user can mark a task complete/incomplete.

**Independent Test** (manual):
- Create a task, call `PATCH /api/tasks/{task_id}/complete`, and confirm it toggles; refresh and confirm persistence.

### Backend

- [X] T051 [US3] Implement PATCH /api/tasks/{task_id}/complete per contract (toggle is_completed) with ownership enforcement: backend/src/api/routes/tasks.py
- [X] T052 [US3] Add Task service method to toggle completion and persist updated_at: backend/src/services/task_service.py

### Frontend

- [X] T053 [US3] Add completion toggle action to TaskItem UI and call PATCH endpoint: frontend/src/components/TaskItem.tsx
- [X] T054 [US3] Add visual completion indicator and ensure it persists on refresh: frontend/src/components/TaskItem.tsx

**Checkpoint**: Completion toggle works end-to-end and persists.

---

## Phase 7: Polish & Cross-Cutting Concerns (Deployment + E2E)

**Purpose**: Containerization, environment templates, and end-to-end validation per spec.

- [X] T055 [P] Add backend Dockerfile (uvicorn, install deps, healthcheck): backend/Dockerfile
- [X] T056 [P] Add frontend Dockerfile (Next.js production build + start): frontend/Dockerfile
- [X] T057 Add root docker-compose.yml wiring frontend + backend and Neon DATABASE_URL passthrough: docker-compose.yml
- [X] T058 Add root .env.example with DATABASE_URL, JWT_SECRET, ports, NEXT_PUBLIC_API_URL: .env.example
- [X] T059 Validate quickstart steps match actual compose/service ports and update if needed: specs/002-fullstack-web-app/quickstart.md

### End-to-End validation checklist (execute after T055-T059)

- [X] T060 Run docker-compose up and verify /health responds 200: docker-compose.yml
- [X] T061 Validate user registration/login + task CRUD + completion toggle via browser UI: frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T062 Validate multi-user isolation with two accounts end-to-end: backend/src/services/task_service.py

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) → Foundational (Phase 2) → US1 (Phase 3)
- US2 (Phase 4) depends on US1 (must have JWT auth usable by API client)
- US4 (Phase 5) depends on US2 (adds/validates enforcement across task endpoints)
- US3 (Phase 6) depends on US2 (toggle operates on tasks)
- Polish (Phase 7) depends on all desired stories being complete

### User Story Dependencies

- US1 is the MVP authentication foundation.
- US2 builds core task management on top of US1.
- US4 hardens US2 against cross-user access.
- US3 extends US2 with completion toggle behavior.

---

## Parallel Examples

### Setup / Foundational (where safe)

```text
Task: "T005 [P] Add backend/src/ package skeleton per plan.md: backend/src/__init__.py"
Task: "T006 [P] Add frontend/src/ skeleton per plan.md: frontend/src/app/layout.tsx"

Task: "T012 [P] Create backend API package structure: backend/src/api/__init__.py"
Task: "T013 [P] Create backend routes package structure: backend/src/api/routes/__init__.py"

Task: "T016 [P] Implement SQLModel User table model per data-model.md: backend/src/models/user.py"
Task: "T017 [P] Implement SQLModel Task table model per data-model.md: backend/src/models/task.py"
```

### User Story 2 (frontend tasks can parallelize)

```text
Task: "T043 [P] [US2] Implement TaskList component: frontend/src/components/TaskList.tsx"
Task: "T044 [P] [US2] Implement TaskForm component: frontend/src/components/TaskForm.tsx"
Task: "T045 [P] [US2] Implement TaskItem component: frontend/src/components/TaskItem.tsx"
```

---

## Implementation Strategy

### MVP First (US1 only)

1. Complete Phase 1 (Setup) and Phase 2 (Foundational)
2. Complete Phase 3 (US1)
3. Stop and validate US1 independent test steps before proceeding

### Incremental Delivery

1. Add US2 → validate CRUD
2. Add US4 → validate isolation
3. Add US3 → validate completion toggle
4. Containerize + run E2E checks (Phase 7)
