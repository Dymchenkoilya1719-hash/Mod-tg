"""Tests for encryption/decryption."""

import pytest
import os
from pathlib import Path
from core.crypto import SessionCrypto


def test_encrypt_decrypt_session(tmp_path):
    """Test session encryption and decryption."""
    test_data = {
        "session_string": "abc123xyz",
        "user_id": 123456,
        "phone": "+1234567890"
    }
    password = "MySecurePassword123!"
    session_file = tmp_path / "test_session.tg"
    
    # Test encryption
    assert SessionCrypto.encrypt_session(
        test_data,
        password,
        str(session_file)
    )
    assert session_file.exists()
    
    # Test decryption
    decrypted = SessionCrypto.decrypt_session(str(session_file), password)
    assert decrypted is not None
    assert decrypted["user_id"] == test_data["user_id"]
    assert decrypted["phone"] == test_data["phone"]


def test_decrypt_with_wrong_password(tmp_path):
    """Test decryption with wrong password."""
    test_data = {"user_id": 123456}
    password = "CorrectPassword123"
    wrong_password = "WrongPassword456"
    session_file = tmp_path / "test_session.tg"
    
    # Encrypt
    SessionCrypto.encrypt_session(test_data, password, str(session_file))
    
    # Try decrypt with wrong password
    decrypted = SessionCrypto.decrypt_session(str(session_file), wrong_password)
    assert decrypted is None


def test_encrypt_session_creates_file(tmp_path):
    """Test that encrypt_session creates file with correct structure."""
    test_data = {"test": "data"}
    password = "password123"
    session_file = tmp_path / "test.tg"
    
    SessionCrypto.encrypt_session(test_data, password, str(session_file))
    
    # Read raw file
    with open(session_file, 'rb') as f:
        file_content = f.read()
    
    # First 16 bytes should be salt
    assert len(file_content) > 16
    salt = file_content[:16]
    assert len(salt) == 16
