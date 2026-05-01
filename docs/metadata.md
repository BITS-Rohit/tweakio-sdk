# Metadata Enums

`camouchat-core` exports lightweight metadata enums for standardizing configurations across independent plugins.

## `Platform` Enum

Identifies the active execution platform for the session and directories.

```python
from camouchat_core import Platform

print(Platform.WHATSAPP)
```

## `StorageType` Enum

Defines the database architecture used for a given profile sandbox.

```python
from camouchat_core import StorageType

# Supported Definitions:
# StorageType.SQLITE
# StorageType.MYSQL
# StorageType.POSTGRESQL
```

## `MessageType` Enum

Identifies the classification of a message payload, essential for routing and processing.

```python
from camouchat_core import MessageType

# Examples:
# MessageType.TEXT
# MessageType.IMAGE
# MessageType.CAMOU_CIPHERTEXT
```

## `MediaType` Enum

Identifies standard media types across all supported platforms.

```python
from camouchat_core import MediaType

# Examples:
# MediaType.IMAGE
# MediaType.VIDEO
# MediaType.DOCUMENT
```
