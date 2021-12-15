from typing import Optional
from uuid import UUID

from app.models import Subject
from pydantic import BaseModel, Field

from .school import ReadSchoolSchema
from .teacher import ReadTeacherSchema
from .term import ReadTermSchema


class BaseSubjectSchema(BaseModel):
    name: str = Field(..., max_length=Subject.MAX_LENGTH_NAME)
    credits: float
    syllabus_url: Optional[str] = Field(
        None, max_length=Subject.MAX_LENGTH_SYLLABUS_URL
    )
    category: Optional[str] = Field(None, max_length=Subject.MAX_LENGTH_CATEGORY)
    type: Optional[str] = Field(None, max_length=Subject.MAX_LENGTH_TYPE)
    target_grade: Optional[int] = Field(None, ge=1, le=5)
    target_department: Optional[UUID] = Field(None)

    class Config:
        orm_mode = True


class ReadSubjectSchema(BaseSubjectSchema):
    uuid: UUID
    term: ReadTermSchema
    teacher: ReadTeacherSchema
    school: ReadSchoolSchema


class ReadSimpleSubjectSchema(BaseSubjectSchema):
    uuid: UUID


class CreateSubjectSchema(BaseSubjectSchema):
    term_uuid: UUID
    teacher_uuid: UUID
    school_uuid: UUID
    target_department_uuid: Optional[UUID] = Field(None)


class UpdateSubjectSchema(BaseSubjectSchema):
    term_uuid: UUID
    teacher_uuid: UUID
    school_uuid: UUID
