from sqlmodel import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.task import Task
from uuid import UUID
from datetime import datetime
from typing import List, Optional

async def create_task(session: AsyncSession, user_id: UUID, title: str, description: Optional[str] = None) -> Task:
    task = Task(
        user_id=user_id,
        title=title,
        description=description
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_tasks(
    session: AsyncSession,
    user_id: UUID,
    is_completed: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Task]:
    statement = select(Task).where(Task.user_id == user_id)

    if is_completed is not None:
        statement = statement.where(Task.is_completed == is_completed)

    statement = statement.order_by(desc(Task.created_at)).limit(limit).offset(offset)
    result = await session.execute(statement)
    return result.scalars().all()

async def get_task_by_id(session: AsyncSession, user_id: UUID, task_id: UUID) -> Optional[Task]:
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def update_task(
    session: AsyncSession,
    user_id: UUID,
    task_id: UUID,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Optional[Task]:
    task = await get_task_by_id(session, user_id, task_id)
    if not task:
        return None

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description

    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def delete_task(session: AsyncSession, user_id: UUID, task_id: UUID) -> bool:
    task = await get_task_by_id(session, user_id, task_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True

async def toggle_task_completion(session: AsyncSession, user_id: UUID, task_id: UUID) -> Optional[Task]:
    task = await get_task_by_id(session, user_id, task_id)
    if not task:
        return None

    task.is_completed = not task.is_completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
