from pydantic import BaseModel, Field
from typing import Optional


class TodoBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field("", max_length=500)
    is_completed: Optional[bool] = Field(False)


class TodoCreate(TodoBase):
    pass


# class TodoCreate(TodoBase):
#     pass


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field("", max_length=500)
    is_completed: Optional[bool] = Field(False)
