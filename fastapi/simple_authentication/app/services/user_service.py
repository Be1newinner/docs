from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate
from pydantic import UUID4
from app.core.security import get_password_hash


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def get_user_by_id(self, user_id: UUID4) -> User | None:
        result = await self.db.get(User, user_id)
        return result

    async def get_user_by_username(self, user_name: str) -> User | None:
        stmt = select(User).where(User.username == user_name)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_user(self, user_input: UserCreate):

        existing_user_by_username = await self.get_user_by_username(user_input.username)
        if existing_user_by_username:
            raise ValueError(f"User with username {user_input.username} already exist!")

        existing_user_by_email = await self.get_user_by_email(user_input.email)
        if existing_user_by_email:
            raise ValueError(f"User with email {user_input.email} already exist!")

        hashed_password = get_password_hash(user_input.password)
        user_input.password = hashed_password

        user_model = User(**user_input.model_dump(), is_active=True)
        self.db.add(user_model)

        try:
            await self.db.commit()
            await self.db.refresh(user_model)
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("Username or Email already registered!")
        return user_model

    async def update_user(self, user_input: UserUpdate, user_id: UUID4):
        user_in_db = await self.get_user_by_id(user_id)
        if not user_in_db:
            return None
        user_input_dict = user_input.model_dump(exclude_unset=True)

        if "password" in user_input_dict:
            del user_input_dict["password"]

        if "id" in user_input_dict:
            del user_input_dict["id"]

        if "role" in user_input_dict:
            del user_input_dict["role"]

        for key, value in user_input.model_dump(exclude_unset=True).items():
            setattr(user_in_db, key, value)

        await self.db.commit()
        await self.db.refresh(user_in_db)
        return user_in_db

    async def change_user_status_by_admin(self, user_id: int):
        pass
