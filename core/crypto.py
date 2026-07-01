"""Encryption utilities for session storage (AES-256)."""

import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
from pathlib import Path


class SessionCrypto:
    """Handle encrypted session storage."""
    
    SALT_SIZE = 16
    ITERATIONS = 100000
    
    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=SessionCrypto.ITERATIONS,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    @staticmethod
    def encrypt_session(session_data: dict, password: str, output_path: str) -> bool:
        """Encrypt session data and save to file.
        
        Args:
            session_data: Dictionary with session info
            password: Password for encryption
            output_path: Path to save encrypted file
            
        Returns:
            True if successful
        """
        try:
            # Generate random salt
            salt = os.urandom(SessionCrypto.SALT_SIZE)
            
            # Derive key from password
            key = SessionCrypto._derive_key(password, salt)
            
            # Create cipher
            cipher = Fernet(key)
            
            # Serialize and encrypt data
            json_data = json.dumps(session_data).encode()
            encrypted_data = cipher.encrypt(json_data)
            
            # Combine salt + encrypted data
            file_content = salt + encrypted_data
            
            # Save to file
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(file_content)
            
            return True
        except Exception as e:
            print(f"[ERROR] Failed to encrypt session: {e}")
            return False
    
    @staticmethod
    def decrypt_session(file_path: str, password: str) -> dict:
        """Decrypt session from file.
        
        Args:
            file_path: Path to encrypted session file
            password: Password for decryption
            
        Returns:
            Decrypted session dict or None
        """
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # Extract salt and encrypted data
            salt = file_content[:SessionCrypto.SALT_SIZE]
            encrypted_data = file_content[SessionCrypto.SALT_SIZE:]
            
            # Derive key using same salt and password
            key = SessionCrypto._derive_key(password, salt)
            
            # Decrypt
            cipher = Fernet(key)
            json_data = cipher.decrypt(encrypted_data)
            
            # Deserialize
            session_data = json.loads(json_data.decode())
            return session_data
        except Exception as e:
            print(f"[ERROR] Failed to decrypt session: {e}")
            return None


if __name__ == "__main__":
    # Example usage
    test_data = {"session_string": "abc123xyz", "user_id": 123456}
    password = "MySecurePassword123!"
    
    # Encrypt
    SessionCrypto.encrypt_session(test_data, password, "test_session.tg")
    print("[✓] Session encrypted")
    
    # Decrypt
    decrypted = SessionCrypto.decrypt_session("test_session.tg", password)
    print(f"[✓] Session decrypted: {decrypted}")
