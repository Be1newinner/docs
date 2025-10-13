### Core Setup & Concepts

1.  **Asynchronous Operations:** In FastAPI, you'll almost always be working with `async/await`. This means our SQLAlchemy setup needs to use the `asyncio` extension and an asynchronous PostgreSQL driver (like `asyncpg`). Synchronous blocking calls will hurt your API's performance and scalability.
2.  **Dependency Injection:** FastAPI's dependency injection system (`Depends`) is crucial for managing database sessions cleanly and ensuring they are properly closed after each request.
3.  **SQLAlchemy 2.0 `select()`:** Forget `session.query()`. In SQLAlchemy 2.0, all primary query building is done via `sqlalchemy.select()`.
4.  **`session.execute()`:** This is how you run your `select()` constructs against the database.
5.  **`scalars()` vs. `all()` vs. `one()` vs. `scalar_one_or_none()`:** Understand how to extract results from the `Result` object returned by `execute()`.
      * `.scalars()`: Used for selecting a single column or ORM object, allowing you to iterate over them directly.
      * `.all()`: Returns a list of tuples, where each tuple represents a row.
      * `.one()`: Expects exactly one result; raises `NoResultFound` or `MultipleResultsFound`.
      * `.one_or_none()`: Expects at most one result; returns `None` if no result.
      * `.scalar_one_or_none()`: Like `one_or_none()`, but specifically for queries that select a single column/entity, returning the scalar value directly.

Let's start with the basic setup and then dive into CRUD.
Alright, let's get into the specifics.

### 1\. Project Structure and Dependencies

First, ensure you have the necessary packages installed:

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy "asyncpg<0.29.0" pydantic
```

  * `asyncpg` is the asynchronous PostgreSQL driver. Note the version constraint, as `asyncpg>=0.29.0` might have breaking changes with some older SQLAlchemy async features, though 2.0.41 should be fine. It's good practice to be explicit.
  * `uvicorn[standard]` includes `httptools` and `watchfiles` for better performance and auto-reloading.

A typical project structure for a mid-sized FastAPI application often looks like this:

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py       # DB engine, session, Base, and dependency
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic schemas for request/response validation
│   └── crud.py           # Database interaction logic (functions for models)
└── requirements.txt
```

### 2\. `database.py`: SQLAlchemy Async Setup

This file will contain your `AsyncEngine`, `AsyncSessionLocal`, and the dependency for getting a session.

```python
# app/database.py
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# PostgreSQL connection string
# postgresql+asyncpg://user:password@host:port/database_name
DATABASE_URL = "postgresql+asyncpg://postgres:your_password@localhost:5432/fastapi_db"

# Create an asynchronous engine
# `echo=True` logs all SQL queries, useful for debugging
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a sessionmaker for AsyncSession
# `expire_on_commit=False` allows access to objects after the session commits
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False # Typically set to False for explicit flushing
)

Base = declarative_base()

# Dependency to get an async database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

**FAANG-level Guidance:**

  * **`expire_on_commit=False`**: This is crucial. If `expire_on_commit` is `True` (the default for `sessionmaker`), ORM objects become "expired" after a `commit()`, meaning accessing their attributes would trigger a new database query. For FastAPI, where you often return objects directly after creation/update, setting this to `False` prevents unnecessary additional queries and makes object management smoother.
  * **`autoflush=False`**: This gives you explicit control over when pending changes are flushed to the database. While `autoflush=True` can be convenient, `False` promotes a clearer separation of concerns and avoids unintended side effects during complex operations. You'll explicitly call `session.flush()` when needed or rely on `session.commit()` to flush implicitly.
  * **`async_sessionmaker`**: Always use `async_sessionmaker` for asynchronous SQLAlchemy.
  * **`get_db` dependency:** This pattern ensures that a new session is created for each request and automatically closed (or rolled back if an error occurs) via the `async with` block, preventing resource leaks.

### 3\. `models.py`: SQLAlchemy ORM Models

Here's an example of a `Product` model. We'll use `Mapped` and `mapped_column` for type-hinted column definitions, which is the modern SQLAlchemy 2.0 style.

```python
# app/models.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Text, func, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
```

**FAANG-level Guidance:**

  * **Type Hinting (`Mapped`):** Embrace `Mapped` for clear, explicit type definitions, especially with `mypy` or other type checkers.
  * **`mapped_column`:** Use `mapped_column` for column definitions, as it offers additional ORM-specific configurations.
  * **`server_default=func.now()` and `onupdate=func.now()`:** This offloads timestamp management to the database, making it more reliable and consistent. `func.now()` uses the database's `NOW()` function.
  * **`nullable=True/False`:** Explicitly define nullability. SQLAlchemy will infer `nullable=False` if not specified and the Python type hint isn't `Optional`.
  * **`index=True`:** Add indexes to frequently queried columns (`name`, `id` by default) for performance.

### 4\. `schemas.py`: Pydantic Models

These define the data shapes for API requests and responses.

```python
# app/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0

class ProductCreate(ProductBase):
    pass # No additional fields for creation

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

class ProductInDB(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) # Enables ORM mode for Pydantic V2
```

**FAANG-level Guidance:**

  * **Separation of Concerns:** Clearly separate your SQLAlchemy ORM models (`models.py`) from your Pydantic schemas (`schemas.py`). ORM models define the database schema, while Pydantic schemas define the API contract. This prevents coupling and allows for different data representations.
  * **`ConfigDict(from_attributes=True)` (Pydantic V2):** This is the equivalent of `orm_mode = True` in Pydantic V1 and is essential for Pydantic to read data directly from ORM objects (e.g., `ProductInDB.from_orm(db_product)` or just passing the ORM object where `response_model` is set to `ProductInDB`).

### 5\. `crud.py`: Database Interaction Functions

This is where your SQLAlchemy queries live, abstracted away from your FastAPI routes.

```python
# app/crud.py
from typing import List, Optional
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload # For relationships (covered later)

from . import models, schemas

### CREATE Operations

async def create_product(db: AsyncSession, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(**product.model_dump()) # Pydantic V2: .model_dump()
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product) # Loads any database-generated values (like id, timestamps)
    return db_product

### READ Operations

# 1. Get a single document by its Primary Key (ID)
async def get_product_by_id(db: AsyncSession, product_id: int) -> Optional[models.Product]:
    # `session.get()` is the most efficient way to get by primary key
    # It checks the identity map first, then queries the database.
    return await db.get(models.Product, product_id)

# 2. Get all documents
async def get_all_products(db: AsyncSession) -> List[models.Product]:
    stmt = select(models.Product)
    result = await db.execute(stmt)
    return result.scalars().all() # .scalars() for ORM objects, .all() to get a list

# 3. Get documents with Limit and Offset (for pagination)
async def get_products_paginated(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[models.Product]:
    stmt = select(models.Product).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# 4. Get documents by filtering a specific column (e.g., by name)
async def get_product_by_name(db: AsyncSession, product_name: str) -> Optional[models.Product]:
    stmt = select(models.Product).where(models.Product.name == product_name)
    result = await db.execute(stmt)
    return result.scalars().first() # .first() gets the first result or None

# 5. Get documents using 'LIKE' for partial string matching
async def search_products_by_name(db: AsyncSession, search_term: str, skip: int = 0, limit: int = 10) -> List[models.Product]:
    # Case-insensitive LIKE using .ilike()
    stmt = (
        select(models.Product)
        .where(models.Product.name.ilike(f"%{search_term}%"))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

# 6. Get documents with multiple filters (AND condition)
async def get_products_by_price_and_stock(
    db: AsyncSession, min_price: float, max_price: float, min_stock: int
) -> List[models.Product]:
    stmt = (
        select(models.Product)
        .where(
            and_(
                models.Product.price >= min_price,
                models.Product.price <= max_price,
                models.Product.stock_quantity >= min_stock
            )
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()

# 7. Get documents with OR condition
async def get_products_by_name_or_description(db: AsyncSession, term: str) -> List[models.Product]:
    stmt = (
        select(models.Product)
        .where(
            or_(
                models.Product.name.ilike(f"%{term}%"),
                models.Product.description.ilike(f"%{term}%")
            )
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()

# 8. Filter by IN clause
async def get_products_by_ids(db: AsyncSession, product_ids: List[int]) -> List[models.Product]:
    stmt = select(models.Product).where(models.Product.id.in_(product_ids))
    result = await db.execute(stmt)
    return result.scalars().all()

### UPDATE Operations

async def update_product(
    db: AsyncSession, product_id: int, product_update: schemas.ProductUpdate
) -> Optional[models.Product]:
    db_product = await db.get(models.Product, product_id)
    if db_product:
        # Update attributes only if they are provided in the Pydantic model
        for key, value in product_update.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)
        await db.commit()
        await db.refresh(db_product) # Refresh to get updated_at from DB
    return db_product

### DELETE Operations

async def delete_product(db: AsyncSession, product_id: int) -> bool:
    db_product = await db.get(models.Product, product_id)
    if db_product:
        await db.delete(db_product)
        await db.commit()
        return True
    return False

# 2. Delete with `where` clause (more efficient for bulk delete)
async def delete_products_by_name_pattern(db: AsyncSession, name_pattern: str) -> int:
    # Build a DELETE statement directly
    # `synchronize_session='fetch'` means SQLAlchemy will fetch the rows to be deleted
    # before deleting them, which allows ORM objects in the session to be correctly
    # expunged/invalidated. 'evaluate' is faster but less reliable if objects are in session.
    # 'False' is fastest but doesn't synchronize session.
    stmt = models.Product.__table__.delete().where(models.Product.name.ilike(f"%{name_pattern}%"))
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount # Returns the number of rows deleted

```

**FAANG-level Guidance:**

  * **`async/await` everywhere:** All database operations (`db.execute`, `db.commit`, `db.refresh`, `db.delete`, `db.get`) must be `await`ed.
  * **`db.refresh()`:** After `db.add()` or `db.commit()`, `db.refresh()` is crucial. It reloads the object's attributes from the database, ensuring you get any default values (like `id` for auto-incrementing primary keys) or `server_default`/`onupdate` timestamps that were set by the database.
  * **`select().where(...)`:** This is the standard way to build `SELECT` queries with filters.
  * **`result.scalars().all()` vs. `result.scalars().first()`:** Know when to use each. `.all()` for lists, `.first()` for a single expected result (or `None`).
  * **`and_`, `or_`:** Use `sqlalchemy.and_` and `sqlalchemy.or_` for explicit logical combinations in your `where` clauses.
  * **`ilike()`:** Use `ilike()` for case-insensitive `LIKE` queries, which is typically preferred for user-facing search.
  * **`delete(db_object)` vs. `table.delete().where(...)`:**
      * `db.delete(db_object)`: Ideal for deleting a single object you've already loaded into the session. It's conceptually clear.
      * `models.Product.__table__.delete().where(...)`: More efficient for *bulk deletes* where you don't need to load all objects into memory first. It issues a direct `DELETE` statement. Use `result.rowcount` to get the number of deleted rows.