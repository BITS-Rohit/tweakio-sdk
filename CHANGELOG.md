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
- **Test Infrastructure**: Isolated interactive E2E and validation scripts from the core automated test suite to streamline CI/CD workflows.
- **Stealth Bridge Extension**: Expanded the internal RAM-level bridge to include typing presence and legacy media decryption stubs for enhanced API parity.

### Changed
- **Unified Media Pipeline**: Standardized media extraction schemas across all processing layers, ensuring consistent metadata and latency telemetry.
- **Stealth Extraction**: Optimized core retrieval logic to natively handle structured results from internal browser caches with enhanced performance metrics.
- **Architecture**: Relocated decorator modules to `WhatsApp/` for a more cohesive and modular package structure.
- **Serialization**: Improved data serialization for binary `Uint8Array` types, ensuring reliable profile and media key extraction.

### Fixed
- **Codebase Hardening**: Achieved 100% type-strictness across 82 source files and hardened the logging infrastructure with robust concurrency fallbacks.
- **Unit Test Stability**: Synchronized `ReplyCapable` functional tests with recent UX renames and structured data requirements.
- **Initialization Logic**: Resolved minor indentation and initialization races in the `CamoufoxBrowser` and `ProfileManager` layers.
- **Data Fidelity**: Eliminated extraction latency and "uncertainty" in message fetching by transitioning to direct memory-resident lookups.

### Removed
- **Redundant Telemetry**: Eliminated verbose media extraction diagnostic prints from production logs to ensure clean operations.
- **Legacy Components**: Deprecated the monolithic `ChatProcessor` scraping logic and early `BrowserForge` wrapper versions.


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
