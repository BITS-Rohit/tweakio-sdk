"""
Unit tests for Encryption module.
"""
import pytest

from src.Encryption import MessageEncryptor, MessageDecryptor, KeyManager
from cryptography.exceptions import InvalidTag


class TestMessageEncryptor:
    """Test cases for MessageEncryptor."""

    def test_encryptor_init_valid_key(self):
        """Test encryptor initialization with valid key."""
        key = b'0' * 32
        encryptor = MessageEncryptor(key)
        assert encryptor.key == key

    def test_encryptor_init_invalid_key(self):
        """Test encryptor initialization with invalid key length."""
        with pytest.raises(ValueError, match="Key must be 32 bytes"):
            MessageEncryptor(b'short_key')

    def test_encrypt_decrypt_string(self):
        """Test basic encryption and decryption of string."""
        key = MessageEncryptor.generate_key()
        encryptor = MessageEncryptor(key)
        decryptor = MessageDecryptor(key)

        plaintext = "Hello, World!"
        nonce, ciphertext = encryptor.encrypt(plaintext)
        decrypted = decryptor.decrypt(nonce, ciphertext)

        assert decrypted == plaintext

    def test_encrypt_decrypt_with_associated_data(self):
        """Test encryption with associated data."""
        key = MessageEncryptor.generate_key()
        encryptor = MessageEncryptor(key)
        decryptor = MessageDecryptor(key)

        plaintext = "Secret message"
        associated_data = b"message_id_123"

        nonce, ciphertext = encryptor.encrypt(plaintext, associated_data)
        decrypted = decryptor.decrypt(nonce, ciphertext, associated_data)

        assert decrypted == plaintext

    def test_encrypt_decrypt_with_wrong_associated_data_fails(self):
        """Test that wrong associated data causes decryption failure."""
        key = MessageEncryptor.generate_key()
        encryptor = MessageEncryptor(key)
        decryptor = MessageDecryptor(key)

        plaintext = "Secret message"
        associated_data = b"message_id_123"

        nonce, ciphertext = encryptor.encrypt(plaintext, associated_data)

        with pytest.raises(InvalidTag):
            decryptor.decrypt(nonce, ciphertext, b"wrong_data")

    def test_encrypt_message_with_id(self):
        """Test encrypt_message method with message ID."""
        key = MessageEncryptor.generate_key()
        encryptor = MessageEncryptor(key)
        decryptor = MessageDecryptor(key)

        message = "Test message"
        message_id = "msg_456"

        nonce, ciphertext = encryptor.encrypt_message(message, message_id)
        decrypted = decryptor.decrypt_message(nonce, ciphertext, message_id)

        assert decrypted == message

    def test_encrypt_empty_string_raises_error(self):
        """Test that encrypting empty string raises error."""
        key = MessageEncryptor.generate_key()
        encryptor = MessageEncryptor(key)

        with pytest.raises(ValueError, match="Plaintext cannot be empty"):
            encryptor.encrypt("")

    def test_nonce_uniqueness(self):
        """Test that each encryption generates unique nonce."""
        key = MessageEncryptor.generate_key()
        encryptor = MessageEncryptor(key)

        nonce1, _ = encryptor.encrypt("message1")
        nonce2, _ = encryptor.encrypt("message2")

        assert nonce1 != nonce2
        assert len(nonce1) == 12
        assert len(nonce2) == 12

    def test_decrypt_with_wrong_nonce_fails(self):
        """Test that using wrong nonce causes decryption failure."""
        key = MessageEncryptor.generate_key()
        encryptor = MessageEncryptor(key)
        decryptor = MessageDecryptor(key)

        plaintext = "Secret message"
        nonce, ciphertext = encryptor.encrypt(plaintext)

        wrong_nonce = b'0' * 12
        with pytest.raises(InvalidTag):
            decryptor.decrypt(wrong_nonce, ciphertext)

    def test_decrypt_with_wrong_key_fails(self):
        """Test that using wrong key causes decryption failure."""
        key1 = MessageEncryptor.generate_key()
        key2 = MessageEncryptor.generate_key()

        encryptor = MessageEncryptor(key1)
        decryptor = MessageDecryptor(key2)

        plaintext = "Secret message"
        nonce, ciphertext = encryptor.encrypt(plaintext)

        with pytest.raises(InvalidTag):
            decryptor.decrypt(nonce, ciphertext)


class TestMessageDecryptor:
    """Test cases for MessageDecryptor."""

    def test_decryptor_init_valid_key(self):
        """Test decryptor initialization with valid key."""
        key = b'0' * 32
        decryptor = MessageDecryptor(key)
        assert decryptor.key == key

    def test_decryptor_init_invalid_key(self):
        """Test decryptor initialization with invalid key length."""
        with pytest.raises(ValueError, match="Key must be 32 bytes"):
            MessageDecryptor(b'short_key')

    def test_decrypt_safe_success(self):
        """Test decrypt_safe with valid data."""
        key = MessageEncryptor.generate_key()
        encryptor = MessageEncryptor(key)
        decryptor = MessageDecryptor(key)

        plaintext = "Test message"
        nonce, ciphertext = encryptor.encrypt(plaintext)

        result = decryptor.decrypt_safe(nonce, ciphertext)
        assert result == plaintext

    def test_decrypt_safe_failure_returns_none(self):
        """Test decrypt_safe with invalid data returns None."""
        key = MessageEncryptor.generate_key()
        encryptor = MessageEncryptor(key)
        decryptor = MessageDecryptor(key)

        plaintext = "Test message"
        nonce, ciphertext = encryptor.encrypt(plaintext)

        result = decryptor.decrypt_safe(nonce, ciphertext, b"wrong_aad")
        assert result is None


class TestKeyManager:
    """Test cases for KeyManager."""

    def test_derive_key_from_password(self):
        """Test key derivation from password."""
        key_manager = KeyManager()
        password = "test_password"
        salt = key_manager.generate_salt()

        key = key_manager.derive_key(password, salt)

        assert len(key) == 32
        assert isinstance(key, bytes)

    def test_derive_key_deterministic(self):
        """Test that same password and salt produce same key."""
        key_manager = KeyManager()
        password = "test_password"
        salt = key_manager.generate_salt()

        key1 = key_manager.derive_key(password, salt)
        key2 = key_manager.derive_key(password, salt)

        assert key1 == key2

    def test_derive_key_different_salts_different_keys(self):
        """Test that different salts produce different keys."""
        key_manager = KeyManager()
        password = "test_password"

        salt1 = key_manager.generate_salt()
        salt2 = key_manager.generate_salt()

        key1 = key_manager.derive_key(password, salt1)
        key2 = key_manager.derive_key(password, salt2)

        assert key1 != key2

    def test_verify_key_success(self):
        """Test key verification with correct password."""
        key_manager = KeyManager()
        password = "test_password"
        salt = key_manager.generate_salt()

        expected_key = key_manager.derive_key(password, salt)
        result = key_manager.verify_key(password, salt, expected_key)

        assert result is True

    def test_verify_key_failure(self):
        """Test key verification with wrong password."""
        key_manager = KeyManager()
        password1 = "password1"
        password2 = "password2"
        salt = key_manager.generate_salt()

        expected_key = key_manager.derive_key(password1, salt)
        result = key_manager.verify_key(password2, salt, expected_key)

        assert result is False

    def test_generate_salt_length(self):
        """Test that generated salt has correct length."""
        key_manager = KeyManager()
        salt = key_manager.generate_salt()

        assert len(salt) == 16

    def test_generate_salt_uniqueness(self):
        """Test that each salt generation is unique."""
        key_manager = KeyManager()

        salt1 = key_manager.generate_salt()
        salt2 = key_manager.generate_salt()

        assert salt1 != salt2

    def test_derive_key_and_salt(self):
        """Test combined key and salt derivation."""
        key_manager = KeyManager()
        password = "test_password"

        salt, key = key_manager.derive_key_and_salt(password)

        assert len(salt) == 16
        assert len(key) == 32
        assert isinstance(key, bytes)

    def test_generate_random_key(self):
        """Test random key generation."""
        key = KeyManager.generate_random_key()

        assert len(key) == 32
        assert isinstance(key, bytes)

    def test_generate_random_key_uniqueness(self):
        """Test that random key generation is unique."""
        key1 = KeyManager.generate_random_key()
        key2 = KeyManager.generate_random_key()

        assert key1 != key2

    def test_derive_key_empty_password_raises_error(self):
        """Test that empty password raises error."""
        key_manager = KeyManager()
        salt = key_manager.generate_salt()

        with pytest.raises(ValueError, match="Password cannot be empty"):
            key_manager.derive_key("", salt)

    def test_derive_key_empty_salt_raises_error(self):
        """Test that empty salt raises error."""
        key_manager = KeyManager()
        password = "test_password"

        with pytest.raises(ValueError, match="Salt must be at least"):
            key_manager.derive_key(password, b"")
