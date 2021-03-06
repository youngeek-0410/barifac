from typing import List, Optional
from uuid import UUID

from app.core.exceptions import (
    ApiException,
    NotFoundObjectMatchingUuid,
    SameObjectAlreadyExists,
)
from app.db.database import get_db_session
from app.models import Department, School
from sqlalchemy.orm import scoped_session

from .base import BaseCRUD
from .school import SchoolCRUD

db_session = get_db_session()


class DepartmentCRUD(BaseCRUD):
    def __init__(self, db_session: scoped_session):
        super().__init__(db_session, Department)

    def get_by_school_and_name(self, school: School, name: str) -> Optional[Department]:
        return self.get_query().filter_by(school_uuid=school.uuid, name=name).first()

    def gets_by_school_uuid(self, school_uuid) -> List[Department]:
        return self.get_query().filter_by(school_uuid=school_uuid).all()

    def create(self, data: dict = {}) -> Department:
        name: str = data["name"]
        school: Optional[School] = SchoolCRUD(db_session).get_by_uuid(
            data["school_uuid"]
        )
        if not school:
            raise ApiException(NotFoundObjectMatchingUuid(School))
        department = self.get_by_school_and_name(school, name)
        if department:
            raise ApiException(SameObjectAlreadyExists)
        return super().create(data)

    def update(self, uuid: UUID, data: dict = {}) -> Department:
        obj = self.get_by_uuid(uuid)
        if obj is None:
            raise ApiException(NotFoundObjectMatchingUuid(Department))

        name: str = data["name"]
        school: Optional[School] = SchoolCRUD(db_session).get_by_uuid(
            data["school_uuid"]
        )
        if not school:
            raise ApiException(NotFoundObjectMatchingUuid(School))
        department = self.get_by_school_and_name(school, name)
        if department and department.uuid != obj.uuid:
            raise ApiException(SameObjectAlreadyExists)
        return super().update(uuid, data)
