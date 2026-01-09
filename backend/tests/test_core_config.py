"""
Tests for Core Configuration Module
"""

import os
from unittest.mock import patch

import pytest

from app.core.config import Settings, get_settings


def test_settings_defaults():
    """Test default settings values."""
    with patch.dict(os.environ, {}, clear=True):
        # Reset cache
        get_settings.cache_clear()
        settings = get_settings()
        assert settings.app_name == "BulkDeal Analyzer API"
        assert settings.app_version == "0.1.0"
        assert settings.debug is False
        assert settings.environment == "development"
        assert settings.api_v1_prefix == "/api/v1"


def test_settings_from_env():
    """Test settings loaded from environment variables."""
    env_vars = {
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_KEY": "test-key",
        "SECRET_KEY": "test-secret-key",
        "DEBUG": "true",
        "ENVIRONMENT": "production",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        # Reset cache
        get_settings.cache_clear()
        settings = get_settings()
        assert settings.supabase_url == "https://test.supabase.co"
        assert settings.supabase_key == "test-key"
        assert settings.secret_key == "test-secret-key"
        assert settings.debug is True
        assert settings.environment == "production"


def test_settings_cors_origins():
    """Test CORS origins default."""
    with patch.dict(os.environ, {}, clear=True):
        get_settings.cache_clear()
        settings = get_settings()
        assert "http://localhost:3000" in settings.cors_origins

