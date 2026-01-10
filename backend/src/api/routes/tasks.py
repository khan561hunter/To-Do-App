from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from ...database import get_session
from ...api.dependencies import get_current_user
from ...models.user import User
from ...services import task_service

router = APIRouter()

# Schema definitions
class TaskCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int

# Route handlers
@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await task_service.create_task(
        session=session,
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description
    )

@router.get("", response_model=TaskListResponse)
async def list_tasks(
    is_completed: Optional[bool] = Query(None),
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    tasks = await task_service.get_tasks(
        session=session,
        user_id=current_user.id,
        is_completed=is_completed,
        limit=limit,
        offset=offset
    )
    # Simplified total for MVP (could be a separate count query)
    return {"tasks": tasks, "total": len(tasks)}

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    task = await task_service.get_task_by_id(session, current_user.id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    task = await task_service.update_task(
        session=session,
        user_id=current_user.id,
        task_id=task_id,
        title=task_data.title,
        description=task_data.description
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    success = await task_service.delete_task(session, current_user.id, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return None

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    task = await task_service.toggle_task_completion(session, current_user.id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task
