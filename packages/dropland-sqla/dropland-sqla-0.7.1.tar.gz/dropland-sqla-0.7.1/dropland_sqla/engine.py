import asyncio
import contextlib
import sys
import threading
from datetime import timedelta
from typing import List, Optional

import ujson
from sqlalchemy import create_engine as create_sync_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.schema import MetaData

from dropland.log import logger, tr
from dropland.storages.sql.base import EngineConfig, NAMING_CONVENTION, \
    SqlStorageBackend, SqlStorageEngine, SqlStorageType


# noinspection PyPep8Naming,PyAbstractClass
class SqlAlchemySyncEngine(SqlStorageEngine):
    def __init__(self, backend, engine, db_type: SqlStorageType, session_class, metadata, timeout: timedelta):
        super().__init__(backend, engine, db_type, timeout)
        self._session_class = session_class
        self._metadata = metadata
        self._lock = threading.Lock()
        self._counter = 0

    @property
    def is_async(self):
        return False

    @property
    def Model(self):
        from .model import SqlaModel, SqlModel

        model = declarative_base(
            metadata=self._metadata, name='SqlModel',
            metaclass=SqlModel, cls=(SqlaModel,)
        )
        model._sql_engine = self

        return model

    @property
    def metadata(self):
        return self._metadata

    def start(self):
        with self._lock:
            if 0 == self._counter:
                logger.info(tr('dropland.storage.sql.engine.started')
                            .format(db_type=self.db_type, async_=f'async=False'))
            self._counter += 1

    def stop(self):
        with self._lock:
            if 1 == self._counter:
                self.raw_engine.dispose()
                logger.info(tr('dropland.storage.sql.engine.stopped')
                            .format(db_type=self.db_type, async_=f'async=False'))
            self._counter = max(self._counter - 1, 0)

    async def async_start(self):
        raise RuntimeError('Use start method')

    async def async_stop(self):
        raise RuntimeError('Use stop method')

    def new_connection(self):
        return self._session_class()

    @contextlib.contextmanager
    def transaction_context(self, connection: Session, autocommit: bool = True):
        tx = connection

        yield tx

        if sys.exc_info()[0]:
            tx.rollback()
        else:
            if autocommit:
                tx.commit()
            else:
                tx.rollback()


# noinspection PyPep8Naming,PyAbstractClass
class SqlAlchemyAsyncEngine(SqlStorageEngine):
    def __init__(self, backend, engine, db_type: SqlStorageType, session_class, metadata, timeout: timedelta):
        super().__init__(backend, engine, db_type, timeout)
        self._session_class = session_class
        self._metadata = metadata
        self._lock = asyncio.Lock()
        self._counter = 0

    @property
    def is_async(self):
        return True

    @property
    def Model(self):
        from .model import SqlaModel, SqlModel

        model = declarative_base(
            metadata=self._metadata, name='SqlModel',
            metaclass=SqlModel, cls=(SqlaModel,)
        )
        model._sql_engine = self

        return model

    @property
    def metadata(self):
        return self._metadata

    def start(self):
        raise RuntimeError('Use async_start method')

    def stop(self):
        raise RuntimeError('Use async_stop method')

    async def async_start(self):
        async with self._lock:
            if 0 == self._counter:
                logger.info(tr('dropland.storage.sql.engine.started')
                            .format(db_type=self.db_type, async_=f'async=True'))
            self._counter += 1

    async def async_stop(self):
        async with self._lock:
            if 1 == self._counter:
                await self.raw_engine.dispose()
                logger.info(tr('dropland.storage.sql.engine.stopped')
                            .format(db_type=self.db_type, async_=f'async=True'))
            self._counter = max(self._counter - 1, 0)

    def new_connection(self):
        return self._session_class()

    @contextlib.asynccontextmanager
    async def async_transaction_context(self, connection: AsyncSession, autocommit: bool = True):
        tx = connection

        yield tx

        if sys.exc_info()[0]:
            await tx.rollback()
        else:
            if autocommit:
                await tx.commit()
            else:
                await tx.rollback()


class SqlAlchemyBackend(SqlStorageBackend):
    @property
    def name(self) -> str:
        return 'sqla'

    @property
    def db_supports(self) -> List[SqlStorageType]:
        return [SqlStorageType.SQLITE, SqlStorageType.POSTGRES, SqlStorageType.MYSQL]

    @property
    def connection_class(self) -> Optional[type]:
        return Session

    @property
    def async_connection_class(self) -> Optional[type]:
        return AsyncSession

    def create_engine(self, db_type: SqlStorageType, config: EngineConfig, use_async: bool) \
            -> Optional['SqlStorageEngine']:
        params = dict(
            echo=config.echo,
            pool_recycle=config.pool_expire_seconds,
            json_serializer=ujson.dumps,
            json_deserializer=ujson.loads,
        )

        if db_type in (SqlStorageType.POSTGRES, SqlStorageType.MYSQL):
            params.update(dict(
                pool_size=config.pool_min_size,
                max_overflow=config.pool_max_size - config.pool_min_size,
                pool_timeout=config.pool_timeout_seconds
            ))

        if use_async:
            engine = create_async_engine(config.url, **params)
            session_class = sessionmaker(engine, autoflush=False, expire_on_commit=False, class_=AsyncSession)
        else:
            engine = create_sync_engine(config.url, **params)
            session_class = sessionmaker(engine, autoflush=False)

        logger.info(tr('dropland.storage.sql.engine.created').format(db_type=db_type, async_=f'async={use_async}'))
        metadata = MetaData(bind=engine, naming_convention=NAMING_CONVENTION)
        engine_class = SqlAlchemyAsyncEngine if use_async else SqlAlchemySyncEngine
        return engine_class(self, engine, db_type, session_class, metadata,
                            timedelta(seconds=config.pool_timeout_seconds))
