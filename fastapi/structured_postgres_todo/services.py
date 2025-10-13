from sqlalchemy.ext.asyncio import AsyncSession
from schemas import TodoBase, TodoCreate, TodoUpdate
from fastapi import Depends
from database import get_db
from model import Todo


async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    todo_data = Todo(**todo.model_dump())
    db.add(todo_data)
    await db.commit()
    await db.refresh(todo_data)
    return todo_data


async def delete_todo(todo: TodoBase, db: AsyncSession = Depends(get_db)):
    pass


async def update_todo(todo: TodoUpdate, db: AsyncSession = Depends(get_db)):
    pass


async def view_todo_by_id(todo: TodoBase, db: AsyncSession = Depends(get_db)):
    pass


async def view_all_todos(todo: TodoBase, db: AsyncSession = Depends(get_db)):
    pass
