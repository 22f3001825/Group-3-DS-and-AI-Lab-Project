"""
api/schemas/auth.py
Request and response models for Google sign-in.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class GoogleLoginRequest(BaseModel):
    """The ID token from `<GoogleLogin>`'s `credentialResponse.credential`.

    Not an OAuth access token — `useGoogleLogin()` returns one of those and it carries no
    verifiable identity claims. The whole backend design depends on this being the ID token.
    """

    credential: str = Field(..., min_length=1, description="Google ID token (JWT)")


class AuthStudent(BaseModel):
    """The signed-in account as the client is allowed to see it."""

    student_id: str
    name: str
    email: Optional[str] = None
    picture_url: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    is_admin: bool = False
    is_active: bool = True
    created_at: Optional[datetime] = None      # member since
    last_login_at: Optional[datetime] = None
    login_count: int = 0

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    student: AuthStudent
