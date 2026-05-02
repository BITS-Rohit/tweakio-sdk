---
name: camouchat-core
description: Core interfaces, protocols, and encryption utilities for the CamouChat SDK.
---

# CamouChat Core SDK - Agent Guide

This file serves as a reference for AI agents interacting with `camouchat-core`. It outlines the available capabilities, protocols, and utilities provided by the core SDK.

## Overview
`camouchat-core` is the foundational layer of the CamouChat SDK. It contains zero platform-specific logic (no WhatsApp or Browser code). Instead, it provides the standard interfaces (Protocols), encryption utilities, and shared metadata that all plugins must implement.

## 1. Contracts (Protocols)
These are the standard interfaces exported by the core. Plugins implement these to ensure compatibility.

- **`ChatProtocol`**: Represents a chat entity (User, Group). Requires `id_serialized`, `name`, `timestamp`.
- **`MessageProtocol`**: Represents a message. Requires `id_serialized`, `timestamp`, `body`, `msgtype`, `from_chat`, `ui`, `encryption_nonce`.
- **`StorageProtocol`**: Interface for database storage. Requires `async def initialize()`, `async def enqueue_insert(msg)`, `async def close()`.
- **`LoginProtocol`**: Interface for authentication flow. Requires `async def verify_login_status()`, `async def handle_login()`.
- **`InteractionControllerProtocol`**: Interface for sending messages. Requires `async def send_text(chat, text)`, `async def open_chat(chat)`.
- **`MediaControllerProtocol`**: Interface for media handling. Requires `async def add_media(file, **kwargs)`.
- **`UiConfigProtocol`**: Interface for DOM/UI element locators.
- **`MessageProcessorProtocol` & `ChatProcessorProtocol`**: Interfaces for data extraction and parsing.

## 2. Encryption (AES-GCM)
The core provides built-in E2E encryption utilities.

- **`KeyManager`**:
  - `generate_random_key() -> bytes`: Generates a secure 32-byte key.
  - `encode_key_for_storage(key: bytes) -> bytes`: Encodes key to base64.
  - `decode_key_from_storage(encoded_key: bytes) -> bytes`: Decodes key from base64.

- **`MessageEncryptor`**:
  - `encrypt_message(message: str, message_id: str) -> tuple[str, str]`: Returns `(ciphertext_b64, nonce_b64)`. The `message_id` is used as Associated Data (AAD).

- **`MessageDecryptor`**:
  - `decrypt_message(encrypted_message: str, nonce: str, message_id: str) -> str`: Decrypts and authenticates the message using the `message_id` as AAD.

## 3. Global Metadata
Shared Enums for cross-plugin consistency.

- **`Platform`**: `WHATSAPP`, `TELEGRAM`, `SIGNAL`, etc.
- **`StorageType`**: `SQLITE`, `POSTGRESQL`.
- **`MessageType`**: `TEXT`, `IMAGE`, `VIDEO`, `DOCUMENT`, `CAMOU_CIPHERTEXT`, etc.
- **`MediaType`**: `TEXT`, `IMAGE`, `VIDEO`, `AUDIO`, `DOCUMENT`.

## 4. Logging
Centralized structured logging.

- **`LoggerFactory`**: Use `LoggerFactory.get_logger("name")` to retrieve a configured logger.
- **`CamouAdapter`**: Wraps the logger to inject consistent context (e.g., profile IDs).

## Usage Rule for Agents
When modifying or extending `camouchat-core`:
1. **NEVER** add platform-specific logic (e.g., WhatsApp selectors) here.
2. Ensure all Protocols use `runtime_checkable` if `isinstance()` checks are needed.
3. Import all core utilities via `from camouchat_core import ...`.
