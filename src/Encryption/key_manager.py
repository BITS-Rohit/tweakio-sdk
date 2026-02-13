"""
Key management module for platform message encryption.

Handles key derivation using Argon2id for secure per-user encryption keys.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id


class KeyManager:
    """
    Manages encryption key derivation using Argon2id.

    Argon2id is a memory-hard key derivation function that provides:
    - Resistance against GPU/ASIC attacks
    - Tunable memory and CPU cost parameters
    - Per-user unique keys from passwords/passphrases

    Security properties:
    - Salt MUST be unique for each user
    - Parameters provide trade-off between security and performance
    - Derived keys should be cached, not recomputed for each operation
    """

    # Default Argon2id parameters (balance security and performance)
    DEFAULT_ITERATIONS = 1
    DEFAULT_LANES = 4
    DEFAULT_MEMORY_COST = 64 * 1024  # 64 MB in KiB
    DEFAULT_KEY_LENGTH = 32  # 256 bits for AES-256

    def __init__(
        self,
        iterations: int = DEFAULT_ITERATIONS,
        lanes: int = DEFAULT_LANES,
        memory_cost: int = DEFAULT_MEMORY_COST,
        key_length: int = DEFAULT_KEY_LENGTH
    ) -> None:
        """
        Initialize key manager with Argon2id parameters.

        Args:
            iterations: Time cost parameter (higher = slower but more secure)
            lanes: Parallelism parameter (number of threads)
            memory_cost: Memory cost in KiB (higher = more memory-hard)
            key_length: Desired key length in bytes (32 for AES-256)
        """
        self.iterations = iterations
        self.lanes = lanes
        self.memory_cost = memory_cost
        self.key_length = key_length

    def derive_key(
        self,
        password: str | bytes,
        salt: bytes
    ) -> bytes:
        """
        Derive encryption key from password using Argon2id.

        Args:
            password: User password or passphrase
            salt: Unique salt for this user (16 bytes recommended)

        Returns:
            Derived encryption key (32 bytes for AES-256)

        Raises:
            ValueError: If salt is empty or password is empty
        """
        if isinstance(password, str):
            password = password.encode('utf-8')

        if not password:
            raise ValueError("Password cannot be empty")

        if not salt or len(salt) < 8:
            raise ValueError("Salt must be at least 8 bytes")

        kdf = Argon2id(
            salt=salt,
            length=self.key_length,
            iterations=self.iterations,
            lanes=self.lanes,
            memory_cost=self.memory_cost,
        )

        return kdf.derive(password)

    def verify_key(
        self,
        password: str | bytes,
        salt: bytes,
        expected_key: bytes
    ) -> bool:
        """
        Verify that password derives to expected key.

        Args:
            password: User password or passphrase
            salt: Salt used during key derivation
            expected_key: Key to verify against

        Returns:
            True if password derives to expected key, False otherwise
        """
        try:
            derived_key = self.derive_key(password, salt)
            return derived_key == expected_key
        except (ValueError, InvalidKey):
            return False

    def generate_salt(self) -> bytes:
        """
        Generate a cryptographically random salt for key derivation.

        Returns:
            16-byte random salt

        Note:
            Salt should be stored alongside encrypted data for key recovery.
            Each user should have a unique salt.
        """
        return os.urandom(16)

    def derive_key_and_salt(
        self,
        password: str | bytes
    ) -> tuple[bytes, bytes]:
        """
        Derive key and generate salt in one operation.

        Args:
            password: User password or passphrase

        Returns:
            Tuple of (salt, derived_key)
        """
        salt = self.generate_salt()
        key = self.derive_key(password, salt)
        return salt, key

    def save_key_to_file(
        self,
        key: bytes,
        filepath: str | Path
    ) -> None:
        """
        Save encryption key to file (use with caution).

        Args:
            key: Encryption key to save
            filepath: Path to save key

        Warning:
            Keys should be stored securely with proper permissions.
            Consider using keyring services or secure vaults instead.
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Write key with restricted permissions
        with open(filepath, 'wb') as f:
            f.write(key)

        # Set file permissions (user read/write only)
        filepath.chmod(0o600)

    def load_key_from_file(
        self,
        filepath: str | Path
    ) -> bytes:
        """
        Load encryption key from file.

        Args:
            filepath: Path to key file

        Returns:
            Encryption key

        Raises:
            FileNotFoundError: If key file does not exist
            ValueError: If key file is corrupted or wrong length
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"Key file not found: {filepath}")

        with open(filepath, 'rb') as f:
            key = f.read()

        if len(key) != self.key_length:
            raise ValueError(
                f"Invalid key length: expected {self.key_length} bytes, "
                f"got {len(key)} bytes"
            )

        return key

    @staticmethod
    def generate_random_key() -> bytes:
        """
        Generate a cryptographically random key directly.

        Returns:
            32-byte random key suitable for AES-256

        Note:
            This method generates a key without key derivation.
            Useful for testing or when using a master key system.
        """
        return os.urandom(32)
