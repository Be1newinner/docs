from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List

DATABASE_URL = "postgresql+asyncpg://admin:admin123@localhost:5432/postgres"

# SQLAlchemy setup
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# DB model
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    completed = Column(Boolean, default=False)

# Pydantic schemas
class TodoCreate(BaseModel):
    title: str
    description: str = ""

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

class TodoOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI(title="Todo API")

# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session

# Startup event to create tables
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# CRUD Routes
@app.post("/todos/", response_model=TodoOut)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    new_todo = Todo(**todo.dict())
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    return new_todo

@app.get("/todos/", response_model=List[TodoOut])
async def get_todos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo))
    return result.scalars().all()

@app.get("/todos/{todo_id}", response_model=TodoOut)
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalar_one_or_none()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoOut)
async def update_todo(todo_id: int, updated: TodoUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalar_one_or_none()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(todo, key, value)
    await db.commit()
    await db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalar_one_or_none()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    await db.delete(todo)
    await db.commit()
    return {"detail": "Todo deleted successfully"}
