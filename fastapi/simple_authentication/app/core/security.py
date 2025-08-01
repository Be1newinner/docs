from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from app.core.config import settings
from jose import jwt, JWTError
from pydantic import UUID4
from typing import Optional
from app.schemas.auth import TokenPayload, Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY)
    return encoded_jwt


def loginTokens(uuid: UUID4) -> dict:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_token(
        data={"sub": str(uuid)}, expires_delta=access_token_expires
    )
    refresh_token = create_token(
        data={"sub": str(uuid)}, expires_delta=refresh_token_expires
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def decode_access_token(token: str) -> Optional[TokenPayload]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY)
        token_data = TokenPayload(**decoded_token)
        return token_data
    except JWTError:
        return None
    except Exception as e:
        return None
