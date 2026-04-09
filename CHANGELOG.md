# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.0] - [Next Version]

### Added
- **Compliance**: Added proper Apache 2.0 attribution and `NOTICE` file for `wa-js` integration.
- **WA-JS Bridge**: Comprehensive RAM-level API for messages, chats, and privacy settings, bypassing DOM scraping.
- **Stealth Engine**: Hardened isolation using non-enumerable properties and randomized identifiers to evade integrity scanners.
- **Media Pipeline**: Automated, multi-category download system (`save_media`) with support for Images, Videos, Audio, and Documents.
- **Extraction Logic**: Stealthy media retrieval using browser Cache API with encrypted blob decryption and CDN fallback.
- **Event Hooks**: `msg_event_hook` decorator for high-performance, real-time message event interception.
- **Data Models**: Extended `ChatModelAPI` and `MessageModelAPI` for full schema parity with internal WhatsApp structures.
- **Precision Reply**: Integrated `WapiSession` into `ReplyCapable` to enable targeted quoting and message focus.
- **Manual Scripts**: Decoupled interactive E2E and Smoke tests from Pytest into standalone scripts (`smoke_script.py`, `script_msgEvent.py`) for cleaner automated CI runs.
- **WAJS Capability**: Added `mark_is_composing` and legacy `decrypt_media` stubs to `WAJS_Scripts` for full API coverage and Mypy compatibility.

- **Unified Media API**: Standardized `extract_media` return schemas across `WapiWrapper`, `MessageApiManager`, and `MediaCapable` for consistent metadata handling.
- **Stealth Extraction**: Optimized `extract_media` logic to natively handle structured results from `wpp.chat.downloadMedia()` with cache/CDN latency tracking.
- **Architecture**: Relocated decorator modules to `WhatsApp/` for a more cohesive package structure.
- **Serialization**: Improved `get_messages` to handle binary `Uint8Array` conversion to base64 for reliable `mediaKey` extraction.

### Fixed
- **Type Safety**: Resolved all remaining Mypy errors across the codebase via proper protocol stubs and type casting.
- **Logging Robustness**: Hardened `camouchat_logger` with conditional `concurrent-log-handler` imports and fallback logic.
- **Unit Test Stability**: Fixed `ReplyCapable` unit tests to align with recent method renames and mock data requirements.
- **Inconsistent Indentation**: Resolved `IndentationError` in `CamoufoxBrowser` initialization logic.
- **Profile Validation**: Corrected platform-level checks in BrowserForge to prevent fingerprint duplication.
- **Data Fidelity**: Eliminated "uncertainty" in message fetching by switching to direct RAM-based extraction.

- **Media Debug Logs**: Removed redundant extraction diagnostic output from `MessageModelAPI.__str__` for clean production logging.
- **Legacy Components**: Removed deprecated `BrowserForge` interface and monolithic `ChatProcessor` scraping logic.


## [0.6.1] - 2026-03-20

### Added

- **Documentation Updates**: Refined all files in the `docs/` directory for better structural clarity.

### Fixed

- **README.md**: Addressed minor content and layout inconsistencies.

## [0.6.0] - 2026-03-20

### Added

- **Anti-Detection Browser Layer**: Integrated [Camoufox](https://github.com/daijro/camoufox) for a stealthy browser core.
- **Dynamic Fingerprinting**: Incorporated [BrowserForge](https://github.com/daijro/browserforge) for realistic browser fingerprinting.
- **Encrypted Storage**: Implemented **AES-GCM-256** encryption for secure local message and credential storage.
- **Multi-Account & Multi-Platform Support**: Enhanced support for managing multiple profiles across Linux, macOS, and Windows.
- **Database Flexibility**: Transitioned to **SQLAlchemy**, supporting SQLite, PostgreSQL, and MySQL.
- **Sandboxed Profiles**: Fully isolated directories per profile for cookies, cache, and fingerprints.
- **Humanized Interaction Layer**: Mimicking real user behavior to reduce detection risks.
- **Dedicated CamouChat Logger**: Color console, rotating file, and JSON logging.
- **OS-Independent Directory Resolve**: Internal management of platform-specific directories.

### Changed

- Major architectural shift to an **interface-driven** design for easier extensibility.
- Improved test coverage to >= 76%.
- Fixed reports for MYPY, Black, Ruff, and deptry.

### Migrated

- **0.1.5 -> 0.6.0**: Significant codebase overhaul, moving from basic automation to a comprehensive, stealth-focused SDK.

## [0.1.5] - 2026-02-01

### Changed

- Final release in the 0.1.x series before the 0.6 core infrastructure overhaul.
