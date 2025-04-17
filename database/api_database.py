import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Pegar a URL do banco de dados a partir da variável de ambiente
DATABASE_URL = os.getenv("API_DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("A variável de ambiente DATABASE_URL não foi encontrada!")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with async_session() as session:
        yield session
