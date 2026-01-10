from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from contextlib import asynccontextmanager
from .database import init_db
from .api.routes import health, auth, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown logic (if any)

app = FastAPI(
    title="Todo App API",
    description="Multi-user authenticated Todo application backend",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])




# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production should restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Todo App API is running"}
