"""
Configuration Management for BulkDeal Analyzer

Handles application settings, environment variables, and configuration.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "BulkDeal Analyzer API"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"

    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:3000"]

    # Database (Supabase)
    # Defaults are for testing/development; override in production via environment variables
    supabase_url: str = "http://localhost:54321"  # Local Supabase default
    supabase_key: str = "test-supabase-key"  # Test key
    supabase_service_role_key: str | None = None

    # Security
    # Default is for testing/development only; must be overridden in production
    secret_key: str = "test-secret-key-change-in-production"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


