"""
api/routers/auth.py
Google Sign-In — the only way into this application.

Two endpoints and no refresh: `POST /auth/google` trades a Google ID token for a session
JWT, `GET /auth/me` reports who that JWT belongs to. When the JWT expires the client is
sent back to the login page, where Google One Tap re-authenticates without a click if the
user's Google session is still alive.

Both handlers are plain `def`, matching the quiz and questions routers: SQLite reads are
blocking and belong in FastAPI's threadpool, not on the event loop.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_current_student
from ..schemas.auth import AuthResponse, AuthStudent, GoogleLoginRequest
from ..services import auth_service
from ...database.models import Student
from ...database.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/google", response_model=AuthResponse)
def sign_in_with_google(body: GoogleLoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    """Verify a Google ID token, upsert the student, and issue a session JWT.

    Every refusal is a different status because the user can only act on one of them:
    503 unconfigured server or Google unreachable · 401 the credential is not valid ·
    403 unverified email, a domain outside the allowlist, or a deactivated account ·
    409 the address already belongs to a row that predates Google sign-in.
    """
    try:
        claims = auth_service.verify_google_credential(body.credential)
        student = auth_service.upsert_student(db, claims)
        token, expires_at = auth_service.issue_token(student)
    except auth_service.AuthNotConfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except auth_service.GoogleUnreachableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except auth_service.InvalidCredentialError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except auth_service.EmailCollisionError as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "email_collision",
                "message": str(exc),
                "existing_student_id": exc.existing_student_id,
            },
        ) from exc
    except (auth_service.EmailNotVerifiedError,
            auth_service.DomainNotAllowedError,
            auth_service.AccountDisabledError) as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc

    return AuthResponse(
        access_token=token,
        expires_at=expires_at,
        student=AuthStudent.model_validate(student),
    )


@router.get("/me", response_model=AuthStudent)
def whoami(current: Student = Depends(get_current_student)) -> AuthStudent:
    """Who this bearer token belongs to, read fresh from the database.

    The client calls this on mount to restore a session, which is also what makes an
    admin demotion or a deactivation visible in the UI within one page load.
    """
    return AuthStudent.model_validate(current)
