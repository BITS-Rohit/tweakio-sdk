# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.7.0] — Unreleased

### Added

- **Plugin Architecture**: Decoupled the monorepo into three independent packages (`camouchat-core`, `camouchat-browser`, `camouchat-whatsapp`) each independently versioned and publishable to PyPI.
- **Protocol Contracts**: Formalized `ChatProtocol`, `MessageProtocol`, `StorageProtocol`, `LoginProtocol`, `InteractionControllerProtocol`, `MediaControllerProtocol`, `UiConfigProtocol`, `MessageProcessorProtocol`, and `ChatProcessorProtocol` as the SDK's stable interface layer.
- **Centralized Logger**: Introduced `LoggerFactory` and `CamouAdapter` for a unified, structured logging system consumable across all plugin packages.
- **Metadata Enums**: Added `Platform` and `StorageType` as canonical enums exported from the core SDK.
- **Typed Enums**: Added `MediaType` and `FileTyped` to the core contracts for cross-plugin media classification.
- **Documentation**: Created comprehensive `docs/` with dedicated files for Contracts, Encryption, Metadata, and Logging.

### Changed

- **Interfaces to Contracts**: Moved all abstract interfaces to a `contracts/` module with strict `typing.Protocol` definitions.
- **Concurrent Logging**: Hardened `camouchat_logger` with a graceful conditional import for `concurrent-log-handler`, falling back to a standard rotating handler when unavailable.
- **README**: Updated installation instructions for the decoupled package structure, updated all links to the `CamouChat-Team` GitHub organization.

### Fixed

- **Static Analysis**: Resolved all Mypy type errors across protocol stubs and strict assertions.

### Removed

- **WhatsApp-Specific Code**: Extracted all WhatsApp platform code into `camouchat-whatsapp`.
- **Browser-Specific Code**: Extracted all browser management code into `camouchat-browser`.

---

## [0.6.1] — 2026-03-20

### Added

- **Documentation**: Refined all files in the `docs/` directory for improved clarity and structural consistency.

### Fixed

- **README**: Addressed minor content inaccuracies and formatting inconsistencies.

---

## [0.6.0] — 2026-03-20

### Added

- **Anti-Detection Browser Core**: Integrated [Camoufox](https://camoufox.com/) as the stealth browser foundation.
- **Dynamic Fingerprinting**: Incorporated [BrowserForge](https://github.com/daijro/browserforge) for realistic, per-session browser fingerprint generation.
- **Encrypted Storage**: Implemented AES-GCM-256 encryption for all locally persisted messages and credentials.
- **Multi-Account Support**: Full support for managing isolated profiles across Linux, macOS, and Windows.
- **Database Abstraction**: Introduced a SQLAlchemy-backed storage layer with support for SQLite, PostgreSQL, and MySQL.
- **Profile Sandboxing**: Fully isolated per-profile directories for cookies, cache, and fingerprint state.
- **Structured Logging**: Added a dedicated logger with colour console output, rotating file handler, and JSON formatter.
- **Directory Resolution**: Introduced platform-aware internal directory management.

### Changed

- **Architecture**: Transitioned to an interface-driven design pattern for improved extensibility and testability.
- **Test Coverage**: Raised automated test coverage to ≥ 76%.
- **Static Analysis**: Achieved clean passes under Mypy, Black, Ruff, and deptry.

---

## [0.1.5] — 2026-02-01

Final release in the 0.1.x series prior to the 0.6.0 core infrastructure overhaul.
