from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, schema: UserCreate) -> User:
        existing_email = self.repository.get_by_email(schema.email)

        if existing_email is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        existing_username = self.repository.get_by_username(schema.username)

        if existing_username is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This username is already taken",
            )

        user = User(
            username=schema.username,
            email=schema.email,
            hashed_password=hash_password(schema.password),
            is_active=True,
            role=UserRole.USER,
        )

        return self.repository.create(user)

    def get_users(self) -> list[User]:
        return self.repository.get_all()

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user