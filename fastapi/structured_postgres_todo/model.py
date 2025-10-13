from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from database import Base


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default="")
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"<Todo(id={self.id}, title={self.title}, description={self.description}, is_completed={self.is_completed})>"
