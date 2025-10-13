import os
from typing import List, Optional, AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Boolean, select, text
from pydantic import BaseModel, Field

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://admin:admin123@localhost:5432/postgres")

engine = create_async_engine(DATABASE_URL, echo=False) 
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False)

Base = declarative_base()

# --- DB Model ---
class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default="")
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.completed})>"

# --- Pydantic Schemas (Input/Output Validation) ---
class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255) # Add validation
    description: str = Field("", max_length=1000)

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

class TodoOut(TodoBase):
    id: int
    completed: bool

    class Config:
        from_attributes = True # Prefer from_attributes for Pydantic V2+

# --- Dependency Management ---
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to provide a database session."""
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

# --- FastAPI Application ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events for the application."""
    async with engine.begin() as conn:
        # Check if table exists before creating to prevent errors on restart
        # This is a simple check; for migrations, use Alembic.
        table_exists = await conn.run_sync(
            lambda sync_conn: engine.dialect.has_table(sync_conn, Todo.__tablename__)
        )
        if not table_exists:
            await conn.run_sync(Base.metadata.create_all)
    yield
    # Clean up resources if any on shutdown
    await engine.dispose() # Properly close engine connection pool

app = FastAPI(
    title="Robust Todo API",
    description="A simple Todo API built with FastAPI and SQLAlchemy, demonstrating best practices.",
    version="1.0.0",
    lifespan=lifespan # Use lifespan for better startup/shutdown control
)

# --- CRUD Operations ---
@app.post("/todos/", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    """Creates a new To-Do item."""
    db_todo = Todo(**todo.model_dump()) # Use model_dump for Pydantic V2+
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[TodoOut])
async def read_todos(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Retrieves a list of To-Do items with pagination."""
    result = await db.execute(select(Todo).offset(skip).limit(limit))
    return list(result.scalars().all())

@app.get("/todos/{todo_id}", response_model=TodoOut)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieves a single To-Do item by ID."""
    todo = await db.scalar(select(Todo).where(Todo.id == todo_id))
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoOut)
async def update_todo(todo_id: int, todo_update: TodoUpdate, db: AsyncSession = Depends(get_db)):
    """Updates an existing To-Do item."""
    todo = await db.scalar(select(Todo).where(Todo.id == todo_id))
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    update_data = todo_update.model_dump(exclude_unset=True) # Pydantic V2+
    for key, value in update_data.items():
        setattr(todo, key, value)

    db.add(todo) # Re-add to session to mark as dirty and ensure update
    await db.commit()
    await db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    """Deletes a To-Do item by ID."""
    todo = await db.scalar(select(Todo).where(Todo.id == todo_id))
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    await db.delete(todo)
    await db.commit()
    return # No content for 204