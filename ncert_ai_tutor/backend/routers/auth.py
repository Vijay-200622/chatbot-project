"""Teacher authentication API router."""

from fastapi import APIRouter

from backend.models.schemas import LoginRequest, LoginResponse
from backend.config import settings
from database.crud import create_teacher, verify_teacher

router = APIRouter(prefix="/api/auth", tags=["Auth"])


def _ensure_default_teacher():
    """Create default teacher account if it doesn't exist."""
    try:
        create_teacher("teacher", settings.teacher_default_password)
    except Exception:
        pass  # Already exists


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate a teacher."""
    _ensure_default_teacher()

    user = verify_teacher(request.username, request.password)
    if user:
        return LoginResponse(
            success=True,
            message="Login successful!",
            user_id=user["id"],
        )
    return LoginResponse(
        success=False,
        message="Invalid username or password.",
        user_id=None,
    )
