from fastapi import APIRouter

from .attend_subject import attend_subject_router
from .auth import auth_router
from .department import department_router
from .edit_request import edit_request_router
from .evaluation import evaluation_router
from .school import school_router
from .score import score_router
from .subject import subject_router
from .subject_comment import subject_comment_router
from .teacher import teacher_router
from .teacher_comment import teacher_comment_router
from .term import term_router
from .user import user_router

api_v1_router = APIRouter()
api_v1_router.include_router(user_router, prefix="/users", tags=["users"])
api_v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(school_router, prefix="/schools", tags=["schools"])
api_v1_router.include_router(
    department_router, prefix="/departments", tags=["departments"]
)
api_v1_router.include_router(teacher_router, prefix="/teachers", tags=["teachers"])
api_v1_router.include_router(term_router, prefix="/terms", tags=["terms"])
api_v1_router.include_router(
    attend_subject_router, prefix="/attend_subjects", tags=["attend_subjects"]
)
api_v1_router.include_router(subject_router, prefix="/subjects", tags=["subjects"])
api_v1_router.include_router(
    subject_comment_router, prefix="/subjects_comments", tags=["subject_comments"]
)
api_v1_router.include_router(
    evaluation_router, prefix="/evaluations", tags=["evaluations"]
)
api_v1_router.include_router(
    teacher_comment_router, prefix="/teacher_comment", tags=["teacher_comments"]
)
api_v1_router.include_router(score_router, prefix="/scores", tags=["scores"])
api_v1_router.include_router(
    edit_request_router, prefix="/edit_requests", tags=["edit_requests"]
)
