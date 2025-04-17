from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from database.target_database import get_target_session

def create_dynamic_endpoint(query: str):
    async def dynamic_endpoint(session: AsyncSession = Depends(get_target_session)):
        result = await session.execute(text(query))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]

    return dynamic_endpoint
