"""
In-memory runtime tracker for active profiles.

Used to determine multi-profile behavior without relying on
disk metadata which may become stale during crashes.
"""
ACTIVE_PROFILES = set()

def register(profile_id: str):
    ACTIVE_PROFILES.add(profile_id)

def unregister(profile_id: str):
    ACTIVE_PROFILES.discard(profile_id)

def count() -> int:
    return len(ACTIVE_PROFILES)