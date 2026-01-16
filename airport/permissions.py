import logging
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)

logger = logging.getLogger(__name__)


class IsAdminOrIsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission:
    - Admins have full access.
    - Authenticated users have read-only access.
    - Unauthenticated users have no access.
    """

    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if user and user.is_staff:
            logger.info(f"Admin access granted with method: {method}")
            return True

        if method in SAFE_METHODS and user and user.is_authenticated:
            logger.info(f"Read-only access granted for authenticated")
            return True

        logger.warning(f"Access denied for user with method: {method}")
        return False
