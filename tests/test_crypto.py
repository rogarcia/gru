"""Tests for crypto layer."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from gru.crypto import CryptoManager


@pytest.fixture
def crypto():
    """Create a crypto manager with temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = CryptoManager(Path(tmpdir), iterations=1000)  # Low iterations for testing
        yield manager


def test_initialize(crypto: CryptoManager):
    """Test crypto initialization."""
    assert not crypto.is_initialized()

    crypto.initialize("test_password")

    assert crypto.is_initialized()


def test_encrypt_decrypt(crypto: CryptoManager):
    """Test encryption and decryption."""
    crypto.initialize("test_password")

    plaintext = "secret data"
    ciphertext, nonce = crypto.encrypt(plaintext)

    assert ciphertext != plaintext.encode()
    assert len(nonce) == 12

    decrypted = crypto.decrypt(ciphertext, nonce)
    assert decrypted == plaintext


def test_different_nonces(crypto: CryptoManager):
    """Test that different encryptions produce different nonces."""
    crypto.initialize("test_password")

    _, nonce1 = crypto.encrypt("data")
    _, nonce2 = crypto.encrypt("data")

    assert nonce1 != nonce2


def test_wrong_password_fails():
    """Test that wrong password produces different key."""
    with tempfile.TemporaryDirectory() as tmpdir:
        crypto1 = CryptoManager(Path(tmpdir), iterations=1000)
        crypto1.initialize("password1")

        plaintext = "secret"
        ciphertext, nonce = crypto1.encrypt(plaintext)

        # Same salt, different password
        crypto2 = CryptoManager(Path(tmpdir), iterations=1000)
        crypto2.initialize("password2")

        # Decryption should fail with wrong key
        with pytest.raises((ValueError, Exception)):
            crypto2.decrypt(ciphertext, nonce)


def test_clear(crypto: CryptoManager):
    """Test clearing key from memory."""
    crypto.initialize("test_password")
    assert crypto.is_initialized()

    crypto.clear()
    assert not crypto.is_initialized()


def test_not_initialized_raises(crypto: CryptoManager):
    """Test operations fail when not initialized."""
    with pytest.raises(RuntimeError, match="not initialized"):
        crypto.encrypt("data")

    with pytest.raises(RuntimeError, match="not initialized"):
        crypto.decrypt(b"data", b"nonce")
