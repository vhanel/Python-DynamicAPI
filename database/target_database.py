import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Pegar a URL do banco de dados a partir da variável de ambiente
TARGET_DATABASE_URL = os.getenv("TARGET_DATABASE_URL")

target_engine = create_async_engine(TARGET_DATABASE_URL, echo=True)
TargetSessionLocal = async_sessionmaker(bind=target_engine, expire_on_commit=False)

# Dependency para usar nas APIs dinâmicas
async def get_target_session():
    async with TargetSessionLocal() as session:
        yield session
