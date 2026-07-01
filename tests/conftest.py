"""Pytest configuration and fixtures."""

import pytest
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def api_id():
    """Fixture for API ID."""
    return int(os.getenv("API_ID", "0"))


@pytest.fixture
def api_hash():
    """Fixture for API hash."""
    return os.getenv("API_HASH", "")


@pytest.fixture
def session_password():
    """Fixture for session password."""
    return os.getenv("SESSION_PASSWORD", "test_password")
