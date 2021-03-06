from sqlalchemy import VARCHAR, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from ..models import BaseModelMixin


class Score(BaseModelMixin):
    __tablename__ = "scores"

    attend_subject_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("attend_subjects.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    evaluation_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("evaluations.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    got_score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    MAX_LENGTH_MEMO = 2000
    memo = Column(VARCHAR(MAX_LENGTH_MEMO), nullable=True)
