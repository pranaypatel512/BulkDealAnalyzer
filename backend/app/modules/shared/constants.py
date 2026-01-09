"""
Shared Constants

Common constants used across modules.
"""

# Subscription Tiers
class SubscriptionTier:
    """Subscription tier constants."""

    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


# Deal Types
class DealType:
    """Deal type constants."""

    BUY = "BUY"
    SELL = "SELL"


# User Roles
class UserRole:
    """User role constants."""

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


# API Limits
class APILimits:
    """API rate limits."""

    FREE_TIER_REQUESTS_PER_HOUR = 100
    BASIC_TIER_REQUESTS_PER_HOUR = 1000
    PREMIUM_TIER_REQUESTS_PER_HOUR = 10000
    ENTERPRISE_TIER_REQUESTS_PER_HOUR = 100000


# File Upload Limits
class FileLimits:
    """File upload limits."""

    MAX_FILE_SIZE_MB = 10
    ALLOWED_EXTENSIONS = [".csv", ".xlsx", ".xls"]


