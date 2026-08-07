"""
api/services/auth_service.py
Google Sign-In, and the session tokens the rest of the API authenticates with.

The flow, in one sentence: the browser gets a Google **ID token**, POSTs it to
`/auth/google`, this module verifies it against Google's keys, upserts the `Student` row
from the claims, and hands back an HS256 JWT the client sends as
`Authorization: Bearer <jwt>` on every later call.

Three decisions worth knowing before changing anything here:

- **`student_id` is Google's `sub`.** It is the only claim Google promises is stable and
  never reused. Emails change hands; `sub` does not.
- **The JWT carries `{sub, iat, exp, iss}` and nothing else.** No `is_admin`, no email.
  Authorization is read from the database row on every request, so a demotion or a
  deactivation takes effect on the *next request* rather than at token expiry. A claim
  nobody checks is how stale authorization gets reintroduced later.
- **Nothing here is configured by default.** With `JWT_SECRET` unset every auth endpoint
  returns 503, exactly like `ADMIN_TOKEN` — an unconfigured deployment is closed, not
  wide open.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Any, Optional

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from ...config import AUTH_JWT_TTL_HOURS
from ...database import crud
from ...database.models import Student

load_dotenv()

JWT_ALGORITHM = "HS256"
JWT_ISSUER = "mlt-course-assistant"

# Google's clock and ours are never quite the same. Without a skew allowance a machine a
# few seconds fast gets "Token used too early" and an unexplainable 401 on a token that
# is perfectly valid.
GOOGLE_CLOCK_SKEW_SECONDS = 10


# ── Errors ────────────────────────────────────────────────────────────────────
# Each maps to exactly one status in routers/auth.py. They are distinct types rather
# than one error with a code because "Google is down" (503) and "that token is a forgery"
# (401) are opposite answers and must never collapse into each other.

class AuthError(Exception):
    """Base for everything this module refuses."""


class AuthNotConfiguredError(AuthError):
    """GOOGLE_CLIENT_ID or JWT_SECRET is unset → 503."""


class GoogleUnreachableError(AuthError):
    """Google's token endpoint or JWKS could not be reached → 503, not 401."""


class InvalidCredentialError(AuthError):
    """The credential failed signature / issuer / audience / expiry checks → 401."""


class EmailNotVerifiedError(AuthError):
    """Google minted a token for an address it has not verified → 403."""


class DomainNotAllowedError(AuthError):
    """The account is outside ALLOWED_EMAIL_DOMAINS → 403."""


class AccountDisabledError(AuthError):
    """`students.is_active` is false → 403."""


class EmailCollisionError(AuthError):
    """A pre-Google row already owns this email under a different id → 409.

    `students.email` is unique, so letting the insert proceed would surface as an
    IntegrityError → 500 at login, for whichever user is most likely to be the operator.
    """

    def __init__(self, message: str, existing_student_id: str):
        super().__init__(message)
        self.existing_student_id = existing_student_id


# ── Configuration ─────────────────────────────────────────────────────────────
# Read at call time, not import time: the tests set these per case, and a deployment
# that fills in .env after first boot should not need a code change to be believed.

def google_client_id() -> str:
    return (os.getenv("GOOGLE_CLIENT_ID") or "").strip()


def jwt_secret() -> str:
    return (os.getenv("JWT_SECRET") or "").strip()


def _csv_env(name: str) -> list[str]:
    return [part.strip().lower() for part in (os.getenv(name) or "").split(",") if part.strip()]


def admin_emails() -> list[str]:
    """Addresses that get `is_admin` AND bypass the domain restriction."""
    return _csv_env("ADMIN_EMAILS")


def allowed_email_domains() -> list[str]:
    """Empty means unrestricted — any Google account may sign in.

    Deliberately not defaulting to the course domain: the repo owner signs in with a
    gmail.com address, so a hardcoded institutional restriction would lock them out of
    their own instance on the first deploy.
    """
    return [d.lstrip("@") for d in _csv_env("ALLOWED_EMAIL_DOMAINS")]


def auth_configured() -> bool:
    return bool(google_client_id() and jwt_secret())


def cors_origins() -> list[str]:
    origins = [o.strip() for o in (os.getenv("CORS_ORIGINS") or "").split(",") if o.strip()]
    return origins or ["http://localhost:5173", "http://localhost:4173"]


# ── Google credential verification ────────────────────────────────────────────

@lru_cache(maxsize=1)
def _google_request() -> Any:
    """One transport, reused — it holds the session that caches Google's JWKS."""
    from google.auth.transport import requests as google_requests  # noqa: PLC0415

    return google_requests.Request()


def verify_google_credential(credential: str) -> dict[str, Any]:
    """Verify a Google ID token and return its claims.

    `verify_oauth2_token` checks the signature against Google's published keys, the
    issuer, the audience (our client ID) and the expiry — everything that makes the token
    mean anything. It raises a bare `ValueError` for all of those failures, so the
    interesting work here is separating "the token is bad" (401) from "we could not ask
    Google" (503).
    """
    if not auth_configured():
        raise AuthNotConfiguredError(
            "Google sign-in is not configured: set GOOGLE_CLIENT_ID and JWT_SECRET in .env "
            "and restart the API."
        )
    if not (credential or "").strip():
        raise InvalidCredentialError("No Google credential was supplied.")

    from google.auth import exceptions as google_exceptions  # noqa: PLC0415
    from google.oauth2 import id_token  # noqa: PLC0415

    try:
        claims = id_token.verify_oauth2_token(
            credential,
            _google_request(),
            google_client_id(),
            clock_skew_in_seconds=GOOGLE_CLOCK_SKEW_SECONDS,
        )
    except google_exceptions.TransportError as exc:
        raise GoogleUnreachableError(f"Could not reach Google to verify the sign-in: {exc}") from exc
    except ValueError as exc:
        raise InvalidCredentialError(f"Google rejected the credential: {exc}") from exc
    except Exception as exc:  # noqa: BLE001 — network stacks raise their own zoo
        raise GoogleUnreachableError(f"Google sign-in verification failed: {exc}") from exc

    if not claims.get("sub"):
        raise InvalidCredentialError("Google credential carries no subject claim.")
    return claims


# ── Policy ────────────────────────────────────────────────────────────────────

def _is_admin_email(email: str) -> bool:
    return bool(email) and email.lower() in admin_emails()


def domain_allowed(email: str, hosted_domain: Optional[str]) -> bool:
    """Enforced against the `hd` claim, falling back to the email suffix.

    `hd` is the authoritative signal for a Workspace account — an address there can carry
    a vanity domain the suffix would not match. A consumer Gmail account has no `hd` at
    all, which is why the suffix is checked too rather than instead.
    """
    allowed = allowed_email_domains()
    if not allowed:
        return True
    if _is_admin_email(email):
        return True
    candidates = {(hosted_domain or "").strip().lower()}
    if "@" in (email or ""):
        candidates.add(email.rsplit("@", 1)[1].strip().lower())
    return any(c and c in allowed for c in candidates)


# ── Student upsert ────────────────────────────────────────────────────────────

def upsert_student(db: Session, claims: dict[str, Any]) -> Student:
    """Create or refresh the row for a verified Google account, and stamp the login.

    Every check that can refuse the login happens before anything is written, so a
    rejected sign-in leaves no trace and no half-updated row.
    """
    sub = str(claims.get("sub") or "").strip()
    email = str(claims.get("email") or "").strip().lower()
    hosted = str(claims.get("hd") or "").strip() or None

    if not claims.get("email_verified", False):
        raise EmailNotVerifiedError(
            "This Google account's email address is not verified, so it cannot be used to sign in."
        )
    if not domain_allowed(email, hosted):
        allowed = ", ".join(allowed_email_domains())
        raise DomainNotAllowedError(
            f"Sign-in is restricted to {allowed}. This account ({email}) is outside it."
        )

    student = crud.get_student(db, sub)

    if student is None and email:
        # The email-uniqueness hazard: a legacy row (student_001 and friends) may already
        # carry this address. Insert would raise IntegrityError → 500 at login, so name
        # the colliding row instead and let an operator decide.
        existing = crud.get_student_by_email(db, email)
        if existing is not None and existing.student_id != sub:
            raise EmailCollisionError(
                f"The address {email} already belongs to student '{existing.student_id}', which "
                "predates Google sign-in. Reassign or clear that row's email before signing in.",
                existing.student_id,
            )

    now = datetime.now(timezone.utc)
    is_admin = _is_admin_email(email)

    if student is None:
        student = Student(student_id=sub, name=str(claims.get("name") or email or "Student"))
        student.created_at = now
        student.is_active = True
        student.login_count = 0
        db.add(student)
    elif not student.is_active:
        # Checked here rather than at the dependency alone, so a deactivated account is
        # refused at the door and never gets a token to spend.
        raise AccountDisabledError("This account has been deactivated. Contact the course team.")

    student.name = str(claims.get("name") or student.name or email or "Student")
    student.email = email or student.email
    student.given_name = claims.get("given_name") or None
    student.family_name = claims.get("family_name") or None
    student.picture_url = claims.get("picture") or None
    student.email_verified = True
    student.hosted_domain = hosted
    # Re-derived at every login rather than granted once: dropping an address from
    # ADMIN_EMAILS revokes admin on the next sign-in with no database surgery.
    student.is_admin = is_admin
    student.last_login_at = now
    student.login_count = int(student.login_count or 0) + 1
    student.updated_at = now

    db.commit()
    db.refresh(student)
    return student


# ── Session tokens ────────────────────────────────────────────────────────────

def issue_token(student: Student) -> tuple[str, datetime]:
    """Mint the session JWT. Returns `(token, expires_at)`."""
    secret = jwt_secret()
    if not secret:
        raise AuthNotConfiguredError(
            "JWT_SECRET is not set: sign-in is disabled. Add it to .env and restart the API."
        )
    import jwt  # noqa: PLC0415

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=AUTH_JWT_TTL_HOURS)
    token = jwt.encode(
        {
            "sub": student.student_id,
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp()),
            "iss": JWT_ISSUER,
        },
        secret,
        algorithm=JWT_ALGORITHM,
    )
    return token, expires_at


def decode_token(token: str) -> dict[str, Any]:
    """Decode a session JWT, or raise `InvalidCredentialError`.

    Expiry, signature and issuer are all failures of the same kind from a caller's point
    of view — the client re-authenticates — so they collapse into one error type here and
    one 401 at the dependency.
    """
    secret = jwt_secret()
    if not secret:
        raise AuthNotConfiguredError(
            "JWT_SECRET is not set: sign-in is disabled. Add it to .env and restart the API."
        )
    import jwt  # noqa: PLC0415

    try:
        return jwt.decode(token, secret, algorithms=[JWT_ALGORITHM], issuer=JWT_ISSUER)
    except jwt.PyJWTError as exc:
        raise InvalidCredentialError(f"Session token rejected: {exc}") from exc


def student_from_token(db: Session, token: str) -> Student:
    """Token → the live `Student` row. Every authorization decision starts here."""
    claims = decode_token(token)
    sub = str(claims.get("sub") or "")
    student = crud.get_student(db, sub) if sub else None
    if student is None:
        raise InvalidCredentialError("This session belongs to an account that no longer exists.")
    if not student.is_active:
        raise AccountDisabledError("This account has been deactivated. Contact the course team.")
    return student
