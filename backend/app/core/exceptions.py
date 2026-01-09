"""
Custom Exceptions for BulkDeal Analyzer
"""

from fastapi import HTTPException, status


class BulkDealAnalyzerException(HTTPException):
    """Base exception for BulkDeal Analyzer."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "An error occurred",
    ):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundError(BulkDealAnalyzerException):
    """Resource not found exception."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
        )


class ValidationError(BulkDealAnalyzerException):
    """Validation error exception."""

    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


class AuthenticationError(BulkDealAnalyzerException):
    """Authentication error exception."""

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class AuthorizationError(BulkDealAnalyzerException):
    """Authorization error exception."""

    def __init__(self, detail: str = "Not authorized"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class DatabaseError(BulkDealAnalyzerException):
    """Database error exception."""

    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


