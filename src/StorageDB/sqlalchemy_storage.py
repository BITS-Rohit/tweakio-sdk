"""
Generic SQLAlchemy storage implementation supporting multiple databases.
Uses async operations for non-blocking performance.
"""
from __future__ import annotations

import asyncio
import logging
from typing import List, Dict, Any, Optional

from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker
)

from src.Exceptions.base import StorageError
from src.Interfaces.message_interface import MessageInterface
from src.Interfaces.storage_interface import StorageInterface
from src.StorageDB.models import Base, Message


class SQLAlchemyStorage(StorageInterface):
    """
    Generic SQLAlchemy storage implementation for MessageInterface data.

    Features:
    - Async queue-based batch insertion
    - Background writer task for performance
    - Support for SQLite, PostgreSQL, MySQL via connection string
    - Generic message storage (works with any MessageInterface implementation)

    Connection string examples:
    - SQLite: sqlite+aiosqlite:///path/to/messages.db
    - PostgreSQL: postgresql+asyncpg://user:pass@host/db
    - MySQL: mysql+aiomysql://user:pass@host/db
    """

    def __init__(
            self,
            queue: asyncio.Queue,
            log: logging.Logger,
            database_url: str = "sqlite+aiosqlite:///messages.db",
            batch_size: int = 50,
            flush_interval: float = 2.0,
            echo: bool = False
    ) -> None:
        """
        Initialize SQLAlchemy storage.

        Args:
            queue: Async queue for message batching
            log: Logger instance
            database_url: SQLAlchemy database URL
            batch_size: Max messages before auto-flush
            flush_interval: Seconds before auto-flush even if batch not full
            echo: Enable SQL query logging (for debugging)
        """
        super().__init__(queue=queue, log=log)
        self.database_url = database_url
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.echo = echo

        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None
        self._writer_task: Optional[asyncio.Task] = None
        self._running = False

    @classmethod
    def from_profile(
            cls,
            profile,  # ProfileInfo type (avoiding import)
            queue: asyncio.Queue,
            log: logging.Logger,
            batch_size: int = 50,
            flush_interval: float = 2.0
    ) -> "SQLAlchemyStorage":
        """
        Create storage from ProfileInfo.

        Args:
            profile: ProfileInfo from ProfileManager
            queue: Async queue
            log: Logger
            batch_size: Batch size
            flush_interval: Flush interval

        Returns:
            Configured SQLAlchemyStorage instance
        """
        database_url = f"sqlite+aiosqlite:///{profile.database_path}"
        return cls(
            queue=queue,
            log=log,
            database_url=database_url,
            batch_size=batch_size,
            flush_interval=flush_interval
        )

    async def init_db(self, **kwargs) -> None:
        """Initialize SQLAlchemy engine and session factory."""
        try:
            # Create async engine with connection pooling
            self._engine = create_async_engine(
                self.database_url,
                echo=self.echo,
                pool_pre_ping=True,  # Verify connections before using
                pool_recycle=3600,  # Recycle connections after 1 hour
                pool_size=5,  # Max number of connections in pool
                max_overflow=10,  # Max overflow connections beyond pool_size
                pool_timeout=30  # Seconds to wait for connection from pool
            )

            # Create session factory
            self._session_factory = async_sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False
            )

            self.log.info(f"SQLAlchemy engine initialized: {self.database_url}")
        except Exception as e:
            raise StorageError(f"Failed to initialize database: {e}") from e

    async def create_table(self, **kwargs) -> None:
        """Create tables if not exists."""
        if not self._engine:
            raise StorageError("Database not initialized. Call init_db() first.")

        try:
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            self.log.info("Tables created/verified.")
        except Exception as e:
            raise StorageError(f"Failed to create tables: {e}") from e

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

        # Flush remaining messages on shutdown
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
        """Insert batch of messages into database."""
        if not self._session_factory:
            raise StorageError("Database not initialized.")

        if not msgs:
            return

        # Convert messages to Message models
        message_models = []
        for msg in msgs:
            try:
                model = SQLAlchemyStorage._message_to_model(msg=msg)
                message_models.append(model)
            except Exception as e:
                self.log.warning(f"Failed to convert message: {e}")
                continue

        if not message_models:
            return

        # Insert batch
        session_factory = self._session_factory
        if session_factory is None:
            raise StorageError("Database not initialized.")

        session_factory = self._get_session_factory()
        async with session_factory() as session:
            try:
                session.add_all(message_models)
                await session.commit()
                self.log.debug(f"Inserted {len(message_models)} messages.")
            except IntegrityError:
                # Some messages may already exist (duplicate message_id)
                await session.rollback()
                # Try inserting one by one to skip duplicates
                success_count = 0
                for model in message_models:
                    try:
                        session_factory = self._get_session_factory()
                        async with session_factory() as single_session:
                            single_session.add(model)
                            await single_session.commit()
                            success_count += 1
                    except IntegrityError:
                        continue  # Skip duplicate
                    except Exception as e:
                        self.log.warning(f"Failed to insert message {model.message_id}: {e}")

                self.log.debug(f"Inserted {success_count}/{len(message_models)} messages (some duplicates).")
            except Exception as e:
                await session.rollback()
                self.log.error(f"Batch insert failed: {e}", exc_info=True)
                raise StorageError(f"Batch insert failed: {e}") from e

    @staticmethod
    def _message_to_model(msg: MessageInterface) -> Message:
        """Convert MessageInterface to Message model."""
        message_id = getattr(msg, 'message_id', None) or getattr(msg, 'data_id', 'unknown')
        raw_data = getattr(msg, 'raw_data', '')
        data_type = getattr(msg, 'data_type', None)
        direction = getattr(msg, 'direction', None)
        system_hit_time = getattr(msg, 'system_hit_time', 0.0)

        parent_chat = getattr(msg, 'parent_chat', None)
        parent_chat_name = ''
        parent_chat_id = ''
        if parent_chat:
            parent_chat_name = getattr(parent_chat, 'chatName', '') or getattr(parent_chat, 'chat_name', '')
            parent_chat_id = getattr(parent_chat, 'chatID', '') or getattr(parent_chat, 'chat_id', '')

        return Message(
            message_id=str(message_id),
            raw_data=str(raw_data) if raw_data else '',
            data_type=str(data_type) if data_type else None,
            direction=str(direction) if direction else None,
            parent_chat_name=str(parent_chat_name),
            parent_chat_id=str(parent_chat_id),
            system_hit_time=float(system_hit_time)
        )

    def check_message_if_exists(self, msg_id: str, **kwargs) -> bool:
        """
        Check if message exists by ID (synchronous for quick checks).
        Note: This uses asyncio.run() internally, not recommended in async context.
        Use check_message_if_exists_async() in async code.
        """
        try:
            return asyncio.run(self.check_message_if_exists_async(msg_id))
        except Exception as e:
            self.log.error(f"Existence check failed: {e}")
            return False

    async def check_message_if_exists_async(self, msg_id: str) -> bool:
        """Async version of existence check."""
        if not self._session_factory:
            return False

        session_factory = self._get_session_factory()
        async with session_factory() as session:
            try:
                stmt = select(exists().where(Message.message_id == msg_id))
                result = await session.execute(stmt)
                return result.scalar()
            except Exception as e:
                self.log.error(f"Async existence check failed: {e}")
                return False

    def get_all_messages(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Retrieve all messages from DB (synchronous).
        Uses asyncio.run() internally, not recommended in async context.
        """
        try:
            return asyncio.run(self.get_all_messages_async(**kwargs))
        except Exception as e:
            self.log.error(f"Get all messages failed: {e}")
            return []

    async def get_all_messages_async(self, **kwargs) -> List[Dict[str, Any]]:
        """Async version of get all messages."""
        if not self._session_factory:
            return []

        limit = kwargs.get('limit', 1000)
        offset = kwargs.get('offset', 0)

        session_factory = self._get_session_factory()
        async with session_factory() as session:
            try:
                stmt = (
                    select(Message)
                    .order_by(Message.id.desc())
                    .limit(limit)
                    .offset(offset)
                )
                result = await session.execute(stmt)
                messages = result.scalars().all()
                return [msg.to_dict() for msg in messages]
            except Exception as e:
                self.log.error(f"Async get all messages failed: {e}")
                return []

    async def get_messages_by_chat(self, chat_name: str, **kwargs) -> List[Dict[str, Any]]:
        """Get messages filtered by chat name."""
        if not self._session_factory:
            return []

        limit = kwargs.get('limit', 100)
        session_factory = self._get_session_factory()

        async with session_factory() as session:
            try:
                stmt = (
                    select(Message)
                    .where(Message.parent_chat_name == chat_name)
                    .order_by(Message.id.desc())
                    .limit(limit)
                )
                result = await session.execute(stmt)
                messages = result.scalars().all()
                return [msg.to_dict() for msg in messages]
            except Exception as e:
                self.log.error(f"Get messages by chat failed: {e}")
                return []

    def _get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        if self._session_factory is None:
            raise StorageError("Database not initialized.")
        return self._session_factory

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

        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None
            self.log.info("Database connection closed.")

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
