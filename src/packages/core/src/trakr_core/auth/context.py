"""Request context management using contextvars."""
from contextvars import ContextVar
from typing import Any, Optional

from trakr_core.exceptions import AuthenticationError

_current_user: ContextVar[Optional[Any]] = ContextVar("current_user", default=None)


def set_current_user(user: Any) -> None:
    """Set the current user in the request context.
    
    Args:
        user: User instance to set as current user
    """
    _current_user.set(user)


def get_current_user_from_context() -> Optional[Any]:
    """Get the current user from request context.
    
    Returns:
        Current user instance or None if not set
    """
    return _current_user.get()


def require_current_user() -> Any:
    """Get the current user from context, raising error if not set.
    
    Returns:
        Current user instance
        
    Raises:
        AuthenticationError: If no user in context
    """    
    user = get_current_user_from_context()
    if user is None:
        raise AuthenticationError("No authenticated user in context")
    return user