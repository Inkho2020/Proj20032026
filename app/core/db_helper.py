from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from asyncio import current_task
from app.core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo=False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        # создание фабрики для сессии (создание SessionLocal)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    # дополнительный шаг для привязки session_factory (SessionLocals)  с задачами (current_task)
    # - async_scoped_session создаёт «обёрнутую» сессию,
    # которая автоматически привязывается к текущей синхронной задаче(asyncio.current_task).
    # Это значит, что если у тебя несколько параллельных запросов в FastAPI,
    # у каждого будет своя отдельная сессия, и они не будут мешать друг другу.
    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    # Это функция‑зависимость (dependency), которую можно использовать в эндпоинтах FastAPI через Depends.
    # создание функции для сессии (создание get_db)
    # async def session_dependency(self):
    #     async with self.get_scoped_session() as session:
    #         yield session
    #         await session.remove()
    async def session_dependency(self):
        session = self.get_scoped_session()  # получаем scoped session
        try:
            yield session
        finally:
            await session.remove()


db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
