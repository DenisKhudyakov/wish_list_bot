from config.config import Base, async_session, engine


def connection(func):
    """
    Декоратор для подключения к базе данных
    :param func:
    :return:
    """

    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper


async def create_tables() -> None:
    """
    Функция создания таблицы перед запуском бота
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
