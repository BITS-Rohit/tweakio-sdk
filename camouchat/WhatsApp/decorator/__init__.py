"""
Utility decorators for camouchat operations.

Provides reusable decorators for common patterns like
ensuring UI state, retry logic, and operation guards.
"""

from .msg_event_hook import msg_event_hook

__all__ = ["msg_event_hook"]
