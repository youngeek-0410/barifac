from typing import List, Optional
from uuid import UUID

from app.core.exceptions import (
    ApiException,
    NotFoundObjectMatchingUuid,
    SameObjectAlreadyExists,
)
from app.db.database import get_db_session
from sqlalchemy.orm import scoped_session

from ..models import AttendSubject, Subject, User
from .base import BaseCRUD
from .subject import SubjectCRUD
from .user import UserCRUD

db_session = get_db_session()


class AttendSubjectCRUD(BaseCRUD):
    def __init__(self, db_session: scoped_session):
        super().__init__(db_session, AttendSubject)

    def gets_by_user(self, user: User) -> List[AttendSubject]:
        return self.get_query().filter_by(user_uuid=user.uuid).all()

    def gets_by_user_and_term_uuid(
        self, user: User, term_uuid: UUID
    ) -> List[AttendSubject]:
        return (
            self.get_query()
            .join(Subject)
            .filter(
                Subject.term_uuid == term_uuid, AttendSubject.user_uuid == user.uuid
            )
            .all()
        )

    def get_by_user_and_subject(
        self, user: User, subject: Subject
    ) -> Optional[AttendSubject]:
        return (
            self.get_query()
            .filter_by(
                user_uuid=user.uuid,
                subject_uuid=subject.uuid,
            )
            .first()
        )

    def create(self, data: dict = {}) -> AttendSubject:
        subject: Optional[Subject] = SubjectCRUD(db_session).get_by_uuid(
            data["subject_uuid"]
        )
        if not subject:
            raise ApiException(NotFoundObjectMatchingUuid(Subject))
        user: Optional[User] = UserCRUD(db_session).get_by_uuid(data["user_uuid"])
        if not user:
            raise ApiException(NotFoundObjectMatchingUuid(User))
        attend_subject = self.get_by_user_and_subject(user, subject)
        if attend_subject:
            raise ApiException(SameObjectAlreadyExists)
        return super().create(data)

    def update(self, uuid: UUID, data: dict = {}) -> AttendSubject:
        obj = self.get_by_uuid(uuid)
        if obj is None:
            raise ApiException(NotFoundObjectMatchingUuid(AttendSubject))

        subject: Optional[Subject] = SubjectCRUD(db_session).get_by_uuid(
            data["subject_uuid"]
        )
        if not subject:
            raise ApiException(NotFoundObjectMatchingUuid(Subject))
        user: Optional[User] = UserCRUD(db_session).get_by_uuid(data["user_uuid"])
        if not user:
            raise ApiException(NotFoundObjectMatchingUuid(User))
        attend_subject = self.get_by_user_and_subject(user, subject)
        if attend_subject and attend_subject.uuid != obj.uuid:
            raise ApiException(SameObjectAlreadyExists)
        return super().update(uuid, data)
