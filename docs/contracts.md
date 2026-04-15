# Core Contracts (Protocols)

The `camouchat-core` SDK is built around a decoupled, interface-first design. We use `typing.Protocol` to define strict interfaces allowing custom platform integrations (like `camouchat-whatsapp`) to remain fully interchangeable without relying on concrete implementations.

## Key Protocols

### Core Processing
- **`MessageProcessorProtocol`**: Defines the required lifecycle for manipulating parsing, and saving messages.
- **`ChatProcessorProtocol`**: Required interface for manipulating chat metadata and persistence.
- **`InteractionControllerProtocol`**: Interface for active interactions on the platform (typing, sending messages, resolving links).
- **`MediaControllerProtocol`**: Interface dictating the contract for parsing, downloading, and storing media.

### Data Models
- **`MessageProtocol`**: The fundamental shape of a message block (sender, state, timestamp).
- **`ChatProtocol`**: The schema required to represent a continuous thread or conversation.

### Lifecycle & Storage
- **`StorageProtocol`**: Datastore constraints ensuring platform-agnostic saves/reads.
- **`LoginProtocol`**: Defines QR code parsing and the authentication flow lifecycle.
- **`UiConfigProtocol`**: Interface for customizing visual elements and command line output for the executing orchestrator.

## Typed Enums

- **`MediaType`**: Defines enum boundaries for media.
- **`FileTyped`**: Used to identify specific buffer output patterns for data storage.
