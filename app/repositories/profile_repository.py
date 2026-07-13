from sqlalchemy.orm import (
    Session,
    joinedload,
)

from app.models.profile import Profile


class ProfileRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, profile: Profile) -> Profile:
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return profile

    def get_by_id(
        self,
        profile_id: int,
    ) -> Profile | None:
        return (
            self.db.query(Profile)
            .filter(Profile.id == profile_id)
            .first()
        )

    def get_by_user_id(
        self,
        user_id: int,
    ) -> Profile | None:
        return (
            self.db.query(Profile)
            .filter(Profile.user_id == user_id)
            .first()
        )

    def get_with_user(
        self,
        profile_id: int,
    ) -> Profile | None:
        return (
            self.db.query(Profile)
            .options(joinedload(Profile.user))
            .filter(Profile.id == profile_id)
            .first()
        )

    def update(self, profile: Profile) -> Profile:
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return profile

    def delete(self, profile: Profile) -> None:
        self.db.delete(profile)
        self.db.commit()