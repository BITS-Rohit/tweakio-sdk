# Encryption Services

The Core SDK ships with a secure layer for processing messages in motion and at rest using AES-256-GCM.

## Components

### `KeyManager`
Provides utilities to securely generate 32-byte cryptographic keys and handle safe disk storage logic mapping.

### `MessageEncryptor`
Provides strict encapsulation routines, ensuring a specific nonce generation and payload obfuscation for string models.

### `MessageDecryptor`
The reverse pipeline, authenticating tag bounds and decoding plaintext content back up to the plugin level.

## Usage Example

```python
from camouchat_core import KeyManager, MessageEncryptor, MessageDecryptor

# 1. Provide Key
key = KeyManager.generate_random_key()

# 2. Encrypt
encryptor = MessageEncryptor(key)
nonce, ciphertext = encryptor.encrypt_message("Hello, stealth world!")

# 3. Decrypt
decryptor = MessageDecryptor(key)
plaintext = decryptor.decrypt_message(nonce, ciphertext)
```
