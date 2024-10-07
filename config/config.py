import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if not find_dotenv():
    exit("Файл.env не найден")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEFAULT_COMMANDS = (
    ("/start", "Запуск бота"),
    ("Выбрать подарок", "Вывод выпадающего списка в виде кнопок, чтобы выбрать подарок"),
    ("Создать подарок", "Добавить подарок в базу данных, по умолчанию он не зарезервирован за гостем"),
    ("Вывести список подарков", "Просто текстовый список, в котором можно ознакомиться с каждым подарком"),
    ("Автор бота", "@adv_mf0"),
)
USERNAME_BD = os.getenv("USERNAME_BD")
PASSWORD_BD = os.getenv("PASSWORD_BD")
DB_NAME = os.getenv("DB_NAME")
PORT_BD = os.getenv("PORT_BD")

DATABASE_URL = (
    f"postgresql+asyncpg://{USERNAME_BD}:{PASSWORD_BD}@db:{PORT_BD}/{DB_NAME}"
)
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()
