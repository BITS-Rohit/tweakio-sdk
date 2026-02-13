"""
Generic Implementation for all platforms to use SQLite DB.
Uses async operations via aiosqlite for non-blocking performance.
"""
from __future__ import annotations

import asyncio
import logging
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional

import aiosqlite

from src.Exceptions.base import StorageError
from src.Interfaces.message_interface import MessageInterface
from src.Interfaces.storage_interface import StorageInterface


class SQLITE_DB(StorageInterface):
    """
    Generic SQLite storage implementation for MessageInterface data.
    
    Features:
    - Async queue-based batch insertion
    - Background writer task for performance
    - Generic message storage (works with any MessageInterface implementation)
    """

    def __init__(
            self,
            queue: asyncio.Queue,
            log: logging.Logger,
            db_path: str = "messages.db",
            batch_size: int = 50,
            flush_interval: float = 2.0
    ) -> None:
        """
        Initialize SQLite storage.
        
        Args:
            queue: Async queue for message batching
            log: Logger instance
            db_path: Path to SQLite database file
            batch_size: Max messages before auto-flush
            flush_interval: Seconds before auto-flush even if batch not full
        """
        super().__init__(queue=queue, log=log)
        self.db_path = Path(db_path)
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self._conn: Optional[aiosqlite.Connection] = None
        self._writer_task: Optional[asyncio.Task] = None
        self._running = False

    async def init_db(self, **kwargs) -> None:
        """Initialize SQLite connection asynchronously."""
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = await aiosqlite.connect(str(self.db_path))
            self._conn.row_factory = aiosqlite.Row
            self.log.info(f"SQLite DB initialized at: {self.db_path}")
        except Exception as e:
            raise StorageError(f"Failed to initialize SQLite DB: {e}") from e

    async def create_table(self, **kwargs) -> None:
        """Create messages table if not exists."""
        if not self._conn:
            raise StorageError("Database not initialized. Call init_db() first.")

        table_sql = """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT UNIQUE NOT NULL,
            raw_data TEXT,
            encrypted_message BLOB,
            encryption_nonce BLOB,
            data_type TEXT,
            direction TEXT,
            parent_chat_name TEXT,
            parent_chat_id TEXT,
            system_hit_time REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        index_sql = """
        CREATE INDEX IF NOT EXISTS idx_message_id ON messages(message_id);
        """
        try:
            await self._conn.execute(table_sql)
            await self._conn.execute(index_sql)
            await self._conn.commit()
            self.log.info("Messages table created/verified.")
        except Exception as e:
            raise StorageError(f"Failed to create table: {e}") from e

    async def start_writer(self, **kwargs) -> None:
        """Start background task to consume queue and write batches."""
        if self._writer_task and not self._writer_task.done():
            self.log.warning("Writer task already running.")
            return

        self._running = True
        self._writer_task = asyncio.create_task(self._writer_loop())
        self.log.info("Background writer started.")

    async def _writer_loop(self) -> None:
        """Background loop that consumes queue and writes batches."""
        batch: List[MessageInterface] = []
        last_flush = asyncio.get_event_loop().time()

        while self._running:
            try:
                try:
                    msg = await asyncio.wait_for(
                        self.queue.get(),
                        timeout=self.flush_interval
                    )
                    if isinstance(msg, list):
                        batch.extend(msg)
                    else:
                        batch.append(msg)
                    self.queue.task_done()
                except asyncio.TimeoutError:
                    pass

                current_time = asyncio.get_event_loop().time()
                should_flush = (
                        len(batch) >= self.batch_size or
                        (batch and current_time - last_flush >= self.flush_interval)
                )

                if should_flush and batch:
                    await self._insert_batch_internally(batch)
                    batch.clear()
                    last_flush = current_time

            except Exception as e:
                self.log.error(f"Writer loop error: {e}", exc_info=True)
                await asyncio.sleep(1)

        if batch:
            await self._insert_batch_internally(batch)

    async def enqueue_insert(self, msgs: List[MessageInterface], **kwargs) -> None:
        """Add messages to queue for batch insertion."""
        if not msgs:
            return

        for msg in msgs:
            await self.queue.put(msg)

        self.log.debug(f"Enqueued {len(msgs)} messages for insertion.")

    async def _insert_batch_internally(self, msgs: List[MessageInterface], **kwargs) -> None:
        """Insert batch of messages into DB."""
        if not self._conn:
            raise StorageError("Database not initialized.")

        if not msgs:
            return

        insert_sql = """
        INSERT OR IGNORE INTO messages
        (message_id, raw_data, encrypted_message, encryption_nonce, data_type, direction, parent_chat_name, parent_chat_id, system_hit_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        records = []
        for msg in msgs:
            try:
                record = self._message_to_record(msg)
                records.append(record)
            except Exception as e:
                self.log.warning(f"Failed to convert message: {e}")
                continue

        if not records:
            return

        try:
            await self._conn.executemany(insert_sql, records)
            await self._conn.commit()
            self.log.debug(f"Inserted {len(records)} messages.")
        except Exception as e:
            self.log.error(f"Batch insert failed: {e}", exc_info=True)
            raise StorageError(f"Batch insert failed: {e}") from e

    def _message_to_record(self, msg: MessageInterface) -> tuple:
        """Convert MessageInterface to database record tuple."""
        message_id = getattr(msg, 'message_id', None) or getattr(msg, 'data_id', 'unknown')
        raw_data = getattr(msg, 'raw_data', '')
        encrypted_message = getattr(msg, 'encrypted_message', None)
        encryption_nonce = getattr(msg, 'encryption_nonce', None)
        data_type = getattr(msg, 'data_type', None)
        direction = getattr(msg, 'direction', None)
        system_hit_time = getattr(msg, 'system_hit_time', 0.0)

        parent_chat = getattr(msg, 'parent_chat', None)
        parent_chat_name = ''
        parent_chat_id = ''
        if parent_chat:
            parent_chat_name = getattr(parent_chat, 'chatName', '') or getattr(parent_chat, 'chat_name', '')
            parent_chat_id = getattr(parent_chat, 'chatID', '') or getattr(parent_chat, 'chat_id', '')

        return (
            str(message_id),
            str(raw_data) if raw_data else '',
            bytes(encrypted_message) if encrypted_message else None,
            bytes(encryption_nonce) if encryption_nonce else None,
            str(data_type) if data_type else None,
            str(direction) if direction else None,
            str(parent_chat_name),
            str(parent_chat_id),
            float(system_hit_time)
        )

    def check_message_if_exists(self, msg_id: str, **kwargs) -> bool:
        """Check if message exists by ID (synchronous for quick checks)."""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.execute(
                    "SELECT 1 FROM messages WHERE message_id = ? LIMIT 1",
                    (msg_id,)
                )
                return cursor.fetchone() is not None
        except Exception as e:
            self.log.error(f"Existence check failed: {e}")
            return False

    async def check_message_if_exists_async(self, msg_id: str) -> bool:
        """Async version of existence check."""
        if not self._conn:
            return False

        try:
            cursor = await self._conn.execute(
                "SELECT 1 FROM messages WHERE message_id = ? LIMIT 1",
                (msg_id,)
            )
            row = await cursor.fetchone()
            return row is not None
        except Exception as e:
            self.log.error(f"Async existence check failed: {e}")
            return False

    def get_all_messages(self, **kwargs) -> List[Dict[str, Any]]:
        """Retrieve all messages from DB (synchronous)."""
        limit = kwargs.get('limit', 1000)
        offset = kwargs.get('offset', 0)

        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT * FROM messages ORDER BY id DESC LIMIT ? OFFSET ?",
                    (limit, offset)
                )
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            self.log.error(f"Get all messages failed: {e}")
            return []

    async def get_all_messages_async(self, **kwargs) -> List[Dict[str, Any]]:
        """Async version of get all messages."""
        if not self._conn:
            return []

        limit = kwargs.get('limit', 1000)
        offset = kwargs.get('offset', 0)

        try:
            cursor = await self._conn.execute(
                "SELECT * FROM messages ORDER BY id DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            self.log.error(f"Async get all messages failed: {e}")
            return []

    async def get_messages_by_chat(self, chat_name: str, **kwargs) -> List[Dict[str, Any]]:
        """Get messages filtered by chat name."""
        if not self._conn:
            return []

        limit = kwargs.get('limit', 100)

        try:
            cursor = await self._conn.execute(
                "SELECT * FROM messages WHERE parent_chat_name = ? ORDER BY id DESC LIMIT ?",
                (chat_name, limit)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            self.log.error(f"Get messages by chat failed: {e}")
            return []

    async def close_db(self, **kwargs) -> None:
        """Close connection and stop writer."""
        self._running = False

        if self._writer_task:
            self._writer_task.cancel()
            try:
                await self._writer_task
            except asyncio.CancelledError:
                pass
            self._writer_task = None

        if self._conn:
            await self._conn.close()
            self._conn = None
            self.log.info("SQLite DB connection closed.")

    async def __aenter__(self):
        """Async context manager entry."""
        await self.init_db()
        await self.create_table()
        await self.start_writer()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close_db()
        return False