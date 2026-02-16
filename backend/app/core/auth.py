"""
Authentication Module

Handles Supabase JWT verification and user extraction for protected routes.
"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import Depends, Header

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError


def _get_supabase_client():
    """Lazy import to avoid circular dependency with database module."""
    from supabase import create_client

    settings = get_settings()
    return create_client(url=settings.supabase_url, key=settings.supabase_key)


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> Any:
    """
    Extract and verify the current user from the Authorization header.

    Validates the JWT token with Supabase and returns the authenticated user.
    Use as a FastAPI dependency for protected routes.

    Args:
        authorization: Bearer token from the Authorization header

    Returns:
        Authenticated Supabase user object (gotrue.types.User)

    Raises:
        AuthenticationError: If token is missing, invalid, or expired
    """
    if not authorization:
        raise AuthenticationError("Authorization header is required")

    if not authorization.startswith("Bearer "):
        raise AuthenticationError("Invalid authorization format. Use: Bearer <token>")

    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise AuthenticationError("Token is required")

    try:
        client = _get_supabase_client()
        user_response = client.auth.get_user(token)

        if not user_response or not user_response.user:
            raise AuthenticationError("Invalid or expired token")

        return user_response.user
    except AuthenticationError:
        raise
    except Exception as e:
        raise AuthenticationError(f"Authentication failed: {e!s}") from e


async def get_optional_user(
    authorization: Annotated[str | None, Header()] = None,
) -> Any | None:
    """
    Optionally extract the current user. Returns None if no token is provided.

    Useful for endpoints that work for both authenticated and anonymous users.
    """
    if not authorization:
        return None

    try:
        return await get_current_user(authorization)
    except AuthenticationError:
        return None


# Type aliases for cleaner dependency injection
CurrentUser = Annotated[Any, Depends(get_current_user)]
OptionalUser = Annotated[Any | None, Depends(get_optional_user)]
