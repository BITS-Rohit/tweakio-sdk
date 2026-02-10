# Multi-Account Profile Manager – Design Specification (v0.1.6)

---

## 1. Objective

Design a user-friendly, platform-first Profile Manager that enables seamless multi-account handling while ensuring:

* Platform-organized storage (platforms/{platform}/{profile})
* Explicit and visible file paths
* Safe activation and deletion handling
* Simple and maintainable backup strategy
* Clear console awareness of active profile
* Full backward compatibility
* No over-engineering

This design prioritizes clarity, user control, and long-term maintainability.

---

## 2. Platform-First Directory Structure

### OS-Compliant Base Path

The base directory is resolved using the platformdirs library:

Linux: ~/.local/share/tweakio/
macOS: ~/Library/Application Support/tweakio/
Windows: %APPDATA%/tweakio/

All profile paths are derived from this base directory.

---

### Directory Layout
```
tweakio/
└── platforms/
    ├── whatsapp/
    │   ├── default/
    │   │   ├── metadata.json
    │   │   ├── session.json
    │   │   ├── fingerprint.pkl
    │   │   ├── cookies.json
    │   │   ├── cache/
    │   │   └── backups/
    │   │
    │   ├── support_bot/
    │   │   ├── metadata.json
    │   │   ├── session.json
    │   │   ├── fingerprint.pkl
    │   │   ├── cookies.json
    │   │   ├── cache/
    │   │   └── backups/
    │   │
    │   └── sales_team/
    │       ├── metadata.json
    │       ├── session.json
    │       ├── fingerprint.pkl
    │       ├── cookies.json
    │       ├── cache/
    │       └── backups/
    │
    ├── telegram/
    │   └── news_bot/
    │       ├── metadata.json
    │       ├── session.json
    │       ├── cache/
    │       └── backups/
    │
    └── discord/
        └── community_bot/
            ├── metadata.json
            ├── session.json
            ├── cache/
            └── backups/
 
```
### Design Rationale

* Users can manually browse and inspect profile folders.
* Platform separation prevents confusion.
* Backups are isolated per profile.
* No hidden directories or implicit storage.

---

## 3. Profile Metadata (metadata.json)

Each profile contains a metadata file that explicitly defines its configuration and storage paths.

Example structure:

profile_id: support_bot
name: Support WhatsApp
platform: whatsapp
version: 0.1.6

created_at: ISO timestamp
last_used: ISO timestamp

paths:

* profile_dir: resolved absolute path
* session_file: session.json
* fingerprint_file: fingerprint.pkl
* cookies_file: cookies.json
* cache_dir: cache/
* backup_dir: backups/

backup:

* enabled: true
* max_backups: 10

status:

* is_active: false
* last_active_pid: null
* lock_file: .lock

Key principles:

* All file locations are visible in metadata.
* No hidden storage locations.
* Backup strategy is intentionally simple.
* Active state is explicitly tracked.

---

## 4. Core Runtime Rule

Each platform may have only one active profile at a time.

Activation behavior:

* If another profile for the same platform is active, it is automatically deactivated.
* The previous profile’s lock is released.
* Metadata for both profiles is updated accordingly.
* Console context reflects the new active profile.

Profiles from different platforms may be active independently.

---

## 5. Active State Enforcement

Active state is enforced through:

1. A .lock file stored inside the profile directory.
2. An in-memory registry tracking active profile per platform.

This ensures:

* No concurrent activation conflicts.
* Active profiles cannot be deleted.
* Safe profile switching.
* Clear runtime state management.

---

## 6. Runtime Activation Flow (Concrete Example)

Command:

tweakio profile activate whatsapp support_bot

Execution steps:

1. Resolve absolute path:
   ~/.local/share/tweakio/platforms/whatsapp/support_bot/

2. Load metadata.json.

3. Acquire .lock file for this profile.

4. If another whatsapp profile is active:

   * Release its lock.
   * Update its metadata (is_active = false).

5. Update current profile metadata:

   * is_active = true
   * last_used = current timestamp

6. Initialize Session and BrowserManager using this profile path.

7. Console updates to:
   [whatsapp:support_bot] $

This provides a clear, linear activation sequence without abstraction.

---

## 7. Backup Strategy (Simple and Practical)

Backups are stored at:

platforms/{platform}/{profile}/backups/

Backup behavior:

* Auto-backup enabled by default.
* Keep only the most recent max_backups (default: 10).
* When the limit is exceeded, the oldest backup is deleted.
* Manual backup and restore commands are available.

Commands:

tweakio profile backup whatsapp support_bot
tweakio profile restore whatsapp support_bot

There are no complex retention tiers.
Encryption is out of scope for v0.1.6.

---

## 8. CLI Transparency and User Awareness

Users can inspect profile paths:

tweakio profile path whatsapp support_bot

Example output:

Profile Directory:
~/.local/share/tweakio/platforms/whatsapp/support_bot

Session File:
session.json

Backup Directory:
backups/

Console awareness:

[whatsapp:support_bot] $

The active platform and profile are always visible to the user.

---

## 9. Backward Compatibility and Migration

On first run of v0.1.6:

If legacy single-profile structure exists:

1. Move legacy profile to:
   platforms/whatsapp/default/
2. Generate metadata.json.
3. Enable backups.
4. Notify user via console.

No data loss occurs.
No manual migration required.
Existing CLI commands continue to function.

---

## 10. Internal Component Overview

Single entry point: ProfileManager

ProfileManager responsibilities:

* Platform-aware path resolution
* Active profile registry (per platform)
* Lock manager (.lock handling)
* Metadata handler (read/write metadata.json)
* Backup manager

The architecture remains simple, clear, and maintainable.

---

## 11. Conclusion

This design satisfies all functional and structural requirements:

* Platform-first organization
* Explicit path transparency
* Safe activation and deletion handling
* Simple backup strategy
* Clear runtime activation flow
* Console awareness of active profile
* Full backward compatibility
* No unnecessary complexity

This proposal is ready for architectural approval and implementation in v0.1.6.

---
