"""
Encryption package for Tweakio SDK.

Provides secure encryption and decryption for platform messages using:
- AES-256-GCM for authenticated encryption
- Argon2id for key derivation
- Per-user encryption keys

Usage:
    from src.Encryption import MessageEncryptor, MessageDecryptor, KeyManager

    # Generate key from password
    key_manager = KeyManager()
    salt, key = key_manager.derive_key_and_salt("user_password")

    # Encrypt message
    encryptor = MessageEncryptor(key)
    nonce, ciphertext = encryptor.encrypt_message("Hello, World!")

    # Decrypt message
    decryptor = MessageDecryptor(key)
    plaintext = decryptor.decrypt_message(nonce, ciphertext)
"""

from src.Encryption.encryptor import MessageEncryptor
from src.Encryption.decryptor import MessageDecryptor
from src.Encryption.key_manager import KeyManager

__all__ = [
    "MessageEncryptor",
    "MessageDecryptor",
    "KeyManager",
]
