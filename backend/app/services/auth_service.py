from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        full_name: str,
        email: str,
        password: str
    ):

        existing_user = UserRepository.get_by_email(
            db,
            email
        )

        if existing_user:
            raise ValueError(
                "User already exists"
            )

        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(
                password
            )
        )

        return UserRepository.create(
            db,
            user
        )

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ):

        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            return None

        if not verify_password(
            password,
            user.hashed_password
        ):
            return None

        return user

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str
    ):

        user = AuthService.authenticate_user(
            db,
            email,
            password
        )

        if not user:
            raise ValueError(
                "Invalid credentials"
            )

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }