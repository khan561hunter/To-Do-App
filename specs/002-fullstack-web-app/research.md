# Research & Discovery: Full-Stack Web Application

**Feature**: Full-Stack Web Application
**Branch**: 002-fullstack-web-app
**Date**: 2026-01-03
**Purpose**: Resolve technical unknowns and establish implementation patterns for the full-stack Todo application

---

## Research Task 1: Better Auth Integration Patterns

### Decision: Better Auth v1.x with JWT Strategy

**Research Findings**:

Better Auth is a modern authentication library for Next.js that provides:
- Built-in JWT token generation and management
- Support for Next.js 16+ App Router
- Server-side session management
- Automatic token refresh
- Type-safe authentication hooks

**Implementation Approach**:

1. **Configuration** (`src/auth/better-auth.config.ts`):
   ```typescript
   export const authConfig = {
     jwt: {
       secret: process.env.JWT_SECRET!,
       expiresIn: '7d',
       refreshExpiresIn: '30d'
     },
     providers: {
       credentials: {
         // Email/password authentication
       }
     }
   }
   ```

2. **Session Management**:
   - Better Auth stores JWT in httpOnly cookies (XSS protection)
   - Automatic token refresh when nearing expiration
   - Server-side session validation on protected routes

3. **Token Issuance Flow**:
   - User registers/logs in → Better Auth validates credentials
   - On success → Generates JWT with user claims (user_id, email)
   - JWT stored in httpOnly cookie
   - Frontend reads auth state from Better Auth hooks

**Rationale**: Better Auth provides comprehensive authentication with minimal boilerplate while maintaining security best practices.

**Alternatives Considered**:
- **NextAuth.js**: More mature but heavier, slower iteration, complex configuration
- **Clerk**: Excellent but third-party hosted, potential vendor lock-in
- **Custom JWT**: More control but requires implementing all security features

**References**:
- Better Auth Documentation: https://better-auth.com
- Next.js App Router Authentication: https://nextjs.org/docs/app/building-your-application/authentication

---

## Research Task 2: FastAPI + SQLModel Best Practices

### Decision: Async SQLModel with Connection Pooling

**Research Findings**:

SQLModel combines SQLAlchemy and Pydantic for type-safe ORM operations. For Neon PostgreSQL:

1. **Async Engine Pattern**:
   - Use `asyncpg` driver for async operations
   - Create async engine with connection pooling
   - Async session dependencies for FastAPI endpoints

2. **Connection String Format**:
   ```python
   DATABASE_URL = "postgresql+asyncpg://user:password@host:5432/dbname"
   ```

3. **Session Management Pattern**:
   ```python
   from sqlmodel import SQLModel, create_engine
   from sqlmodel.ext.asyncio.session import AsyncSession

   async_engine = create_async_engine(
       DATABASE_URL,
       echo=True,
       pool_size=10,
       max_overflow=20
   )

   async def get_session() -> AsyncSession:
       async with AsyncSession(async_engine) as session:
           yield session
   ```

**Database Connection Architecture**:

1. **Single Engine Instance**: Created once at app startup, reused across requests
2. **Connection Pooling**: 10 persistent connections, 20 overflow, automatic recycling
3. **Session Per Request**: FastAPI dependency injection creates/closes sessions
4. **Alembic Migrations**: For schema evolution (though MVP may use create_all)

**Middleware Design**:

No database middleware needed - use FastAPI dependencies instead:
- `Depends(get_session)` injects database session
- `Depends(get_current_user)` injects authenticated user

**Rationale**: Async operations prevent blocking during database I/O, connection pooling optimizes resource usage, dependency injection ensures proper session lifecycle.

**Alternatives Considered**:
- **Synchronous SQLModel**: Simpler but blocks on I/O (not scalable)
- **Raw SQLAlchemy**: More control but loses Pydantic validation benefits
- **Tortoise ORM**: Good async support but less mature, smaller ecosystem

**References**:
- SQLModel Documentation: https://sqlmodel.tiangolo.com
- FastAPI with Async SQL: https://fastapi.tiangolo.com/advanced/async-sql-databases/
- Neon Serverless Postgres: https://neon.tech/docs/connect/connect-from-any-app

---

## Research Task 3: JWT Verification on Backend

### Decision: PyJWT Library with HS256 Algorithm

**Research Findings**:

JWT verification requires:
1. Shared secret (same as Better Auth uses)
2. Algorithm specification (HS256 for symmetric signing)
3. Token extraction from Authorization header
4. Claims validation (expiration, issuer)

**Chosen Library**: **PyJWT** (python-jose is alternative but PyJWT is simpler)

**JWT Middleware Implementation Approach**:

```python
# src/middleware/auth_middleware.py
from jose import jwt, JWTError
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )

async def get_current_user(
    payload: dict = Depends(verify_token),
    session: AsyncSession = Depends(get_session)
) -> User:
    user_id = payload.get("user_id")
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

**Token Expiration Handling**:
- PyJWT automatically validates `exp` claim
- Returns JWTError if token expired
- Frontend receives 401, triggers re-authentication

**Shared Secret Management**:
- Environment variable `JWT_SECRET` loaded in both services
- Same value used for signing (Better Auth) and verification (FastAPI)
- Validated at startup (fail fast if missing)

**Rationale**: PyJWT is lightweight, well-maintained, and has excellent FastAPI integration. HS256 is sufficient for symmetric key authentication in this architecture.

**Alternatives Considered**:
- **python-jose**: More features but heavier, includes JOSE protocols we don't need
- **Authlib**: Comprehensive but overkill for simple JWT verification
- **Custom implementation**: Not recommended (security-critical code)

**References**:
- PyJWT Documentation: https://pyjwt.readthedocs.io
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- JWT Best Practices: https://tools.ietf.org/html/rfc8725

---

## Research Task 4: Docker Compose Networking

### Decision: Docker Compose with Named Networks and Service Discovery

**Research Findings**:

Docker Compose provides automatic service discovery via DNS:
- Service names become hostnames (e.g., `backend`, `frontend`)
- Services on same network can communicate directly
- Environment variables injected from `.env` file

**docker-compose.yml Structure**:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - JWT_SECRET=${JWT_SECRET}
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

**Service-to-Service Communication**:
- Frontend → Backend: `http://backend:8000/api/...`
- Backend → Database: Uses `DATABASE_URL` (external Neon)
- Browser → Frontend: `http://localhost:3000`
- Browser → Backend: `http://localhost:8000` (CORS enabled)

**Health Checks**:
- Backend health endpoint: `GET /health` returns 200
- Frontend waits for backend to be healthy via `depends_on`
- Ensures services start in correct order

**Environment Variable Injection**:
- `.env` file at repository root
- Variables loaded automatically by Docker Compose
- Secrets never committed to git (`.env` in `.gitignore`)

**Rationale**: Docker Compose's built-in networking is sufficient for local development. Service discovery via DNS names simplifies configuration. Health checks ensure services are ready before dependent services start.

**Alternatives Considered**:
- **Docker Swarm**: Overkill for local dev, adds complexity
- **Kubernetes**: Production-grade, far too complex for MVP
- **Separate networks per service**: Unnecessary isolation, complicates communication

**References**:
- Docker Compose Networking: https://docs.docker.com/compose/networking/
- Docker Compose Environment Variables: https://docs.docker.com/compose/environment-variables/
- Health Checks: https://docs.docker.com/compose/compose-file/compose-file-v3/#healthcheck

---

## Research Task 5: Next.js 16 App Router + Better Auth

### Decision: Server Components for Layout, Client Components for Interactive UI

**Research Findings**:

Next.js 16 App Router introduces:
- Server Components by default (improved performance)
- Client Components for interactivity (`'use client'` directive)
- Nested layouts for shared UI
- Route groups for organization without affecting URLs

**Frontend Architecture**:

1. **Server Components**:
   - `app/layout.tsx`: Root layout (header, navigation)
   - `app/(auth)/layout.tsx`: Auth pages layout
   - `app/(dashboard)/layout.tsx`: Protected dashboard layout

2. **Client Components**:
   - `components/TaskList.tsx`: Interactive task list
   - `components/TaskForm.tsx`: Task creation/edit form
   - Authentication forms (need state management)

3. **Protected Route Pattern**:
   ```typescript
   // app/(dashboard)/layout.tsx
   import { getSession } from '@/auth/better-auth'
   import { redirect } from 'next/navigation'

   export default async function DashboardLayout({ children }) {
     const session = await getSession()
     if (!session) {
       redirect('/login')
     }
     return <div>{children}</div>
   }
   ```

**API Client with JWT Attachment**:

```typescript
// src/services/api.ts
import { getToken } from '@/auth/better-auth'

export async function apiClient(
  endpoint: string,
  options: RequestInit = {}
) {
  const token = await getToken()
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  })

  if (!response.ok) {
    if (response.status === 401) {
      // Token expired, trigger re-authentication
      window.location.href = '/login'
    }
    throw new Error('API request failed')
  }

  return response.json()
}
```

**Routing Strategy**:
- `/` - Landing page (public)
- `/login` - Login page (public)
- `/register` - Registration page (public)
- `/tasks` - Task dashboard (protected)

**Rationale**: Server Components reduce JavaScript bundle size and improve initial page load. Client Components used only where necessary for interactivity. Route groups organize code without adding URL segments.

**Alternatives Considered**:
- **Pages Router**: Older Next.js pattern, missing App Router benefits
- **All Client Components**: Works but sends more JavaScript, slower initial load
- **All Server Components**: Can't handle user interactions

**References**:
- Next.js App Router: https://nextjs.org/docs/app
- Server vs Client Components: https://nextjs.org/docs/app/building-your-application/rendering/composition-patterns
- Better Auth with App Router: https://better-auth.com/docs/nextjs-app-router

---

## Summary of Key Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Frontend Auth** | Better Auth v1.x with JWT | Modern, type-safe, App Router native |
| **Backend ORM** | Async SQLModel with pooling | Type-safe, async, Pydantic integration |
| **JWT Library** | PyJWT with HS256 | Lightweight, secure, well-maintained |
| **Containerization** | Docker Compose with health checks | Simple orchestration, service discovery |
| **Frontend Architecture** | Server Components + Client Components | Performance optimization, modern patterns |
| **Database Connection** | AsyncEngine with 10/20 pool | Scalable, prevents connection exhaustion |
| **API Security** | JWT verification on every request | Stateless, scalable authentication |

---

## Integration Points Validated

1. ✅ **Frontend ← JWT Token ← Better Auth**: JWT issued on login, stored in httpOnly cookie
2. ✅ **Frontend → API Request → JWT in Header**: API client attaches `Authorization: Bearer <token>`
3. ✅ **Backend → JWT Verification → User Claims**: PyJWT decodes token, extracts user_id
4. ✅ **Backend → Database Query → User-Scoped**: All queries filtered by user_id from JWT
5. ✅ **Docker Compose → Services → Environment Variables**: Shared JWT_SECRET, DATABASE_URL

---

## Open Questions Resolved

**Q1**: How does Better Auth integrate with Next.js 16 App Router?
**A1**: Server-side auth checks in layouts, client-side hooks for interactive components

**Q2**: How to prevent N+1 query problems with SQLModel?
**A2**: Use `selectinload` for eager loading related entities (tasks include user)

**Q3**: Should we use sync or async SQLModel?
**A3**: Async - prevents blocking I/O, essential for scalability

**Q4**: How to handle JWT expiration gracefully?
**A4**: Better Auth auto-refreshes before expiration; backend returns 401 if expired, frontend redirects to login

**Q5**: Docker Compose vs separate containers?
**A5**: Docker Compose - orchestrates multi-container app, simplifies local dev

---

## Implementation Readiness

All research tasks completed. No remaining technical unknowns. Ready to proceed to Phase 1: Design Artifacts.

**Next Steps**:
1. Generate data-model.md with complete database schema
2. Create API contracts in contracts/api-spec.yaml
3. Write quickstart.md for developer onboarding
4. Update agent context with technology stack
