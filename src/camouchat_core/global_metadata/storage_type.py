from enum import StrEnum


class StorageType(StrEnum):
    """Supported storage database dialects."""

    SQLITE = "sqlite"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"

    @staticmethod
    def list_types() -> list[str]:
        """List available storage types."""
        return [t.value for t in StorageType]
