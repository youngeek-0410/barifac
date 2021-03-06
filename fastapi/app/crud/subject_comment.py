from typing import List, Optional
from uuid import UUID

from app.core.exceptions import ApiException, NotFoundObjectMatchingUuid
from app.db.database import get_db_session
from sqlalchemy.orm import scoped_session

from ..models import Subject, SubjectComment
from .base import BaseCRUD
from .subject import SubjectCRUD

db_session = get_db_session()


class SubjectCommentCRUD(BaseCRUD):
    def __init__(self, db_session: scoped_session):
        super().__init__(db_session, SubjectComment)

    def gets_by_subject_uuid(self, subject_uuid: UUID) -> List[SubjectComment]:
        return self.get_query().filter_by(subject_uuid=subject_uuid).all()

    def gets_by_user_uuid(self, user_uuid: UUID) -> List[SubjectComment]:
        return self.get_query().filter_by(user_uuid=user_uuid).all()

    def create(self, data: dict = {}) -> SubjectComment:
        subject: Optional[SubjectComment] = SubjectCRUD(db_session).get_by_uuid(
            data["subject_uuid"]
        )
        if not subject:
            raise ApiException(NotFoundObjectMatchingUuid(Subject))
        return super().create(data)

    def update(self, uuid: UUID, data: dict = {}) -> SubjectComment:
        obj = self.get_by_uuid(uuid)
        if obj is None:
            raise ApiException(NotFoundObjectMatchingUuid(SubjectComment))
        subject: Optional[SubjectComment] = SubjectCRUD(db_session).get_by_uuid(
            data["subject_uuid"]
        )
        if not subject:
            raise ApiException(NotFoundObjectMatchingUuid(Subject))
        return super().update(uuid, data)
