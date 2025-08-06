from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService
from app.core.security import verify_password, loginTokens
from pydantic import UUID4

class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db
        self.user_service = UserService(db)

    async def login_by_email_or_username_and_password(
        self, email_or_username: str, password: str
    ):

        if "@" in email_or_username:
            user_in_db = await self.user_service.get_user_by_email(email_or_username)
        else:
            user_in_db = await self.user_service.get_user_by_username(email_or_username)

        if not user_in_db:
            return {"message": "email, username or password is invalid!"}

        if not user_in_db.is_active:
            return {"message": "User is not active"}

        if not verify_password(password, user_in_db.password):
            return {"message": "email, username or password is invalid!"}

        login_tokens = loginTokens(user_in_db.id)

        return {
            "email": user_in_db.email,
            "username": user_in_db.username,
            "id": user_in_db.id,
            "is_active": user_in_db.is_active,
            "gender": user_in_db.gender,
            "contact": user_in_db.contact,
            "fullname": user_in_db.fullname,
            # "role": user_in_db.role,
            "created_at": user_in_db.created_at,
            "updated_at": user_in_db.updated_at,
            "access_token": login_tokens["access_token"],
        }

    def validate_token(self, user_id: int):
        pass

    def create_password_reset_token(self, user_id: int):
        pass

    def reset_password(self, user_id: int):
        pass

    def invalidate_refresh_token(self, user_id: int):
        pass
