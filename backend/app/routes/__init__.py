from .auth import router as auth_router
from .dashboard import router as dashboard_router
from .subjects import router as subjects_router
from .quizzes import router as quizzes_router
from .recommendations import router as recommendations_router

__all__ = [
    "auth_router", "dashboard_router", "subjects_router",
    "quizzes_router", "recommendations_router",
]
