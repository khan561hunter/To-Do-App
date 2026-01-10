# Data Model: Full-Stack Web Application

**Feature**: Full-Stack Web Application
**Branch**: 002-fullstack-web-app
**Date**: 2026-01-03
**Database**: Neon Serverless PostgreSQL
**ORM**: SQLModel (SQLAlchemy + Pydantic)

---

## Overview

This document defines the complete database schema for the multi-user Todo application. The schema enforces user data isolation through foreign key relationships and supports all functional requirements defined in the specification.

---

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
│─────────────────│
│ id (PK)         │◄──┐
│ email (UNIQUE)  │   │
│ password_hash   │   │
│ created_at      │   │
│ updated_at      │   │
└─────────────────┘   │
                      │ 1:N
                      │
┌─────────────────┐   │
│      Task       │   │
│─────────────────│   │
│ id (PK)         │   │
│ user_id (FK)    │───┘
│ title           │
│ description     │
│ is_completed    │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

---

## Entity Definitions

### User Entity

**Purpose**: Represents an authenticated user account

**Table Name**: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique user identifier |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | User email address (login identifier) |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- PRIMARY KEY on `id` (automatic)
- UNIQUE INDEX on `email` (for login lookups)

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: list["Task"] = Relationship(back_populates="owner")
```

**Validation Rules** (enforced by Pydantic):
- Email must be valid format (RFC 5322)
- Password must be hashed before storage (never store plaintext)
- Email is case-insensitive for lookups (normalized to lowercase)

**Security Considerations**:
- Passwords hashed with bcrypt (cost factor 12)
- No password reset mechanism in MVP (out of scope)
- Email uniqueness prevents duplicate accounts

---

### Task Entity

**Purpose**: Represents a todo item owned by a user

**Table Name**: `tasks`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique task identifier |
| `user_id` | UUID | NOT NULL, FOREIGN KEY → users(id) ON DELETE CASCADE | Owner reference |
| `title` | VARCHAR(200) | NOT NULL | Task title (required) |
| `description` | TEXT | NULL | Optional task description |
| `is_completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- PRIMARY KEY on `id` (automatic)
- INDEX on `user_id` (for user-scoped queries)
- COMPOSITE INDEX on `(user_id, created_at DESC)` (for ordered task lists)

**Foreign Key Constraints**:
- `user_id` → `users(id)` ON DELETE CASCADE
  - When user is deleted, all their tasks are automatically deleted

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    owner: User = Relationship(back_populates="tasks")
```

**Validation Rules** (enforced by Pydantic):
- Title is required, max 200 characters
- Description is optional, unlimited length
- is_completed defaults to False on creation

**Query Patterns**:
- All queries MUST filter by `user_id` (data isolation)
- Task lists ordered by `created_at DESC` (newest first)
- No cross-user queries permitted

---

## Relationships

### User → Tasks (One-to-Many)

**Type**: One-to-Many
**Cardinality**: 1 User → 0..N Tasks
**Cascade**: DELETE CASCADE (deleting user deletes all tasks)

**Implementation**:
- Foreign key `tasks.user_id` references `users.id`
- SQLModel Relationship bidirectional navigation
- Enforced at database level (referential integrity)

**Query Examples**:
```python
# Get all tasks for a user
user_tasks = await session.exec(
    select(Task).where(Task.user_id == user_id)
).all()

# Get user with their tasks (eager loading)
user_with_tasks = await session.exec(
    select(User)
    .where(User.id == user_id)
    .options(selectinload(User.tasks))
).first()
```

---

## Constraints & Invariants

### Database-Level Constraints

1. **Primary Keys**: Auto-generated UUIDs (collision-resistant)
2. **Foreign Keys**: Enforced referential integrity
3. **NOT NULL**: Required fields cannot be null
4. **UNIQUE**: Email uniqueness enforced at database level
5. **DEFAULT VALUES**: Timestamps, completion status have defaults

### Application-Level Constraints

1. **User Data Isolation**: All task queries filtered by `user_id` from JWT
2. **Email Normalization**: Emails lowercased before storage/lookup
3. **Password Security**: Bcrypt hashing (cost 12) before storage
4. **Title Length**: Max 200 characters enforced by Pydantic
5. **UUID Generation**: Uses `uuid4()` for cryptographically random IDs

### Invariants

1. **No Orphaned Tasks**: Cascade delete ensures tasks never exist without owner
2. **Unique Emails**: No two users can have the same email (case-insensitive)
3. **Non-Empty Titles**: Tasks must always have a title (enforced by NOT NULL)
4. **Boolean Completion**: is_completed is always true or false (never null)

---

## Indexes & Performance

### Index Strategy

| Index | Type | Columns | Purpose |
|-------|------|---------|---------|
| `users_pkey` | PRIMARY KEY | `id` | Unique user identification |
| `users_email_idx` | UNIQUE | `email` | Fast login lookups |
| `tasks_pkey` | PRIMARY KEY | `id` | Unique task identification |
| `tasks_user_id_idx` | INDEX | `user_id` | User-scoped task queries |
| `tasks_user_created_idx` | COMPOSITE | `user_id, created_at DESC` | Ordered task lists |

### Query Optimization

1. **User Login** (`SELECT * FROM users WHERE email = ?`):
   - Uses `users_email_idx` (unique index)
   - Single row lookup: O(log n)

2. **List User Tasks** (`SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC`):
   - Uses `tasks_user_created_idx` (composite index)
   - Index covers both filter and sort: O(log n + k) where k = result size

3. **Get Single Task** (`SELECT * FROM tasks WHERE id = ? AND user_id = ?`):
   - Uses `tasks_pkey` for id lookup
   - Additional user_id check ensures ownership (security)

### Performance Characteristics

- **Expected Load**: 100-10k users, 10-1000 tasks per user
- **Query Patterns**: Primarily single-user queries (no joins across users)
- **Scaling Strategy**: Horizontal via connection pooling, vertical if needed

---

## Data Migrations

### Initial Schema Creation

For MVP, use SQLModel's `create_all()`:

```python
from sqlmodel import SQLModel, create_engine

# Create all tables
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### Future Migration Strategy

For production, use Alembic:
- Track schema changes in version-controlled migrations
- Support rollback and forward migrations
- Preserve data during schema evolution

---

## Sample Data

### User Record
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "password_hash": "$2b$12$KIXxLVq8YQJz...",
  "created_at": "2026-01-03T10:00:00Z",
  "updated_at": "2026-01-03T10:00:00Z"
}
```

### Task Record
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete project documentation",
  "description": "Write comprehensive docs for the full-stack app",
  "is_completed": false,
  "created_at": "2026-01-03T11:00:00Z",
  "updated_at": "2026-01-03T11:00:00Z"
}
```

---

## Security Considerations

### Data Isolation

1. **Query Filtering**: All task queries MUST include `WHERE user_id = ?`
2. **Authorization Check**: JWT provides user_id, validated before query
3. **No Cross-User Access**: Database schema doesn't prevent, application enforces

### Password Security

1. **Hashing**: Bcrypt with cost factor 12 (2^12 rounds)
2. **Salt**: Automatic per-password unique salt via bcrypt
3. **No Plaintext Storage**: Passwords never stored unencrypted
4. **No Password in API Responses**: Pydantic models exclude password_hash

### Audit Trail

- `created_at`: Track when entities were created
- `updated_at`: Track last modification (manual update in code)
- Future: Add `deleted_at` for soft deletes (out of MVP scope)

---

## Validation Rules Summary

| Field | Validation | Enforcement Layer |
|-------|------------|-------------------|
| `user.email` | Valid email format, unique | Pydantic + Database |
| `user.password` | Min 8 chars, 1 letter, 1 number | API endpoint (pre-hash) |
| `task.title` | Required, max 200 chars | Pydantic + Database |
| `task.description` | Optional, unlimited | Pydantic |
| `task.user_id` | Must reference existing user | Database FK |
| `task.is_completed` | Boolean only | Pydantic + Database |

---

## API Response Models

### UserResponse (exclude password)
```python
class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime
    # password_hash excluded for security
```

### TaskResponse
```python
class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime
```

### TaskCreate
```python
class TaskCreate(BaseModel):
    title: str = Field(max_length=200)
    description: str | None = None
    # user_id from JWT, not from request body
```

### TaskUpdate
```python
class TaskUpdate(BaseModel):
    title: str | None = Field(None, max_length=200)
    description: str | None = None
    # is_completed updated via separate toggle endpoint
```

---

## Schema Evolution Plan

### MVP (Current)
- 2 tables: users, tasks
- Basic fields only
- UUID primary keys
- Foreign key relationships

### Future Extensions (Post-MVP)
- `task_categories` table for task organization
- `task_due_dates` column for deadlines
- `task_priority` column for importance
- `user_preferences` table for settings
- `shared_tasks` table for collaboration
- `audit_log` table for change tracking

**Note**: All extensions require schema migrations and backward-compatible API changes.

---

## Database Connection Configuration

### Connection String Format
```
postgresql+asyncpg://user:password@host.neon.tech:5432/dbname?sslmode=require
```

### Connection Pool Settings
```python
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set True for SQL logging in dev
    pool_size=10,  # Persistent connections
    max_overflow=20,  # Additional on demand
    pool_pre_ping=True,  # Verify connections
    pool_recycle=3600  # Recycle after 1 hour
)
```

---

## Compliance with Constitution

✅ **Database Rules (Section 10)**:
- Neon PostgreSQL cloud-hosted (no local containers)
- Users and Tasks entities with ownership relationship
- Persistent storage replaces in-memory

✅ **Backend Rules (Section 8)**:
- SQLModel exclusive for database access
- All queries filtered by authenticated user ID
- Foreign key enforces data integrity

✅ **Functional Requirements**:
- FR-017: Neon PostgreSQL persistence ✅
- FR-018: Data persists across sessions ✅
- FR-019: Queries filtered by user_id ✅
- FR-020: Users cannot access other users' tasks ✅
- FR-021: Foreign key relationship enforced ✅

---

## Summary

This data model provides:
- **Type Safety**: SQLModel combines SQLAlchemy and Pydantic
- **Security**: User data isolation via foreign keys and query filtering
- **Performance**: Optimized indexes for common query patterns
- **Maintainability**: Clear relationships and constraints
- **Scalability**: Async operations with connection pooling

**Ready for Implementation**: All entities, relationships, and constraints fully specified. Proceed to API contract generation.
