"""Encryption layer using AES-256-GCM with PBKDF2 key derivation."""

from __future__ import annotations

import os
import secrets
from pathlib import Path
from typing import TYPE_CHECKING

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

if TYPE_CHECKING:
    from gru.db import Database


class CryptoManager:
    """Manages encryption/decryption of secrets using AES-256-GCM."""

    SALT_SIZE = 16
    NONCE_SIZE = 12
    KEY_SIZE = 32  # 256 bits

    def __init__(self, data_dir: Path, iterations: int = 480000) -> None:
        self.data_dir = data_dir
        self.iterations = iterations
        self._key: bytes | None = None
        self._salt_path = data_dir / ".salt"

    def _get_or_create_salt(self) -> bytes:
        """Get existing salt or create new one."""
        if self._salt_path.exists():
            return self._salt_path.read_bytes()
        salt = secrets.token_bytes(self.SALT_SIZE)
        self._salt_path.write_bytes(salt)
        # Restrict permissions
        self._salt_path.chmod(0o600)
        return salt

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.KEY_SIZE,
            salt=salt,
            iterations=self.iterations,
        )
        return kdf.derive(password.encode())

    def initialize(self, master_password: str) -> None:
        """Initialize crypto with master password."""
        salt = self._get_or_create_salt()
        self._key = self._derive_key(master_password, salt)

    def is_initialized(self) -> bool:
        """Check if crypto is initialized."""
        return self._key is not None

    def encrypt(self, plaintext: str) -> tuple[bytes, bytes]:
        """Encrypt plaintext, return (ciphertext, nonce)."""
        if not self._key:
            raise RuntimeError("Crypto not initialized")
        nonce = os.urandom(self.NONCE_SIZE)
        aesgcm = AESGCM(self._key)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
        return ciphertext, nonce

    def decrypt(self, ciphertext: bytes, nonce: bytes) -> str:
        """Decrypt ciphertext using stored nonce."""
        if not self._key:
            raise RuntimeError("Crypto not initialized")
        aesgcm = AESGCM(self._key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()

    def rotate_key(self, old_password: str, new_password: str) -> bytes:
        """Rotate to new master password, return new salt."""
        if not self._key:
            raise RuntimeError("Crypto not initialized")
        # Verify old password works (constant-time comparison)
        old_salt = self._salt_path.read_bytes()
        old_key = self._derive_key(old_password, old_salt)
        if not secrets.compare_digest(old_key, self._key):
            raise ValueError("Old password incorrect")
        # Create new salt and key
        new_salt = secrets.token_bytes(self.SALT_SIZE)
        self._key = self._derive_key(new_password, new_salt)
        self._salt_path.write_bytes(new_salt)
        self._salt_path.chmod(0o600)
        return new_salt

    def clear(self) -> None:
        """Clear key from memory."""
        self._key = None


class SecretStore:
    """High-level interface for storing encrypted secrets."""

    def __init__(self, db: Database, crypto: CryptoManager) -> None:  # noqa: F821
        self.db: Database = db
        self.crypto = crypto

    async def set(self, key: str, value: str) -> None:
        """Store an encrypted secret."""
        if not self.crypto.is_initialized():
            raise RuntimeError("Crypto not initialized")
        ciphertext, nonce = self.crypto.encrypt(value)
        await self.db.store_secret(key, ciphertext, nonce)

    async def get(self, key: str) -> str | None:
        """Retrieve and decrypt a secret."""
        if not self.crypto.is_initialized():
            raise RuntimeError("Crypto not initialized")
        result = await self.db.get_secret(key)
        if result is None:
            return None
        ciphertext, nonce = result
        return self.crypto.decrypt(ciphertext, nonce)

    async def delete(self, key: str) -> bool:
        """Delete a secret."""
        return await self.db.delete_secret(key)

    async def list_keys(self) -> list[str]:
        """List all secret keys."""
        return await self.db.list_secrets()

    async def rotate_all(self, old_password: str, new_password: str) -> int:
        """Rotate master password and re-encrypt all secrets."""
        if not self.crypto.is_initialized():
            raise RuntimeError("Crypto not initialized")
        # Get all secrets decrypted with old key
        keys = await self.list_keys()
        decrypted: dict[str, str] = {}
        for key in keys:
            value = await self.get(key)
            if value is not None:
                decrypted[key] = value
        # Rotate key
        self.crypto.rotate_key(old_password, new_password)
        # Re-encrypt all secrets with new key
        for key, value in decrypted.items():
            await self.set(key, value)
        return len(decrypted)
