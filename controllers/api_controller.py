from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.api_model import Api
from schemas.api_schema import ApiCreate, ApiUpdate
from datetime import datetime

async def list_apis(db: AsyncSession):
    result = await db.execute(select(Api))
    apis = result.scalars().all()
    return apis

async def create_api(db: AsyncSession, api_data: ApiCreate):
    new_api = Api(
        name=api_data.name,
        endpoint=api_data.endpoint,
        sql_query=api_data.sql_query,
        tag=api_data.tag,
        is_active=api_data.is_active,
        created_at=datetime.utcnow()
    )
    db.add(new_api)
    await db.commit()
    await db.refresh(new_api)
    return new_api

async def update_existing_api(db: AsyncSession, api_id: int, api_data: ApiUpdate):
    result = await db.execute(select(Api).where(Api.id == api_id))
    api = result.scalar_one_or_none()

    if not api:
        raise HTTPException(status_code=404, detail="API não encontrada")

    api.name = api_data.name
    api.endpoint = api_data.endpoint
    api.sql_query = api_data.sql_query
    api.tag = api_data.tag
    api.is_active = api_data.is_active
    api.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(api)
    return api

async def delete_existing_api(db: AsyncSession, api_id: int):
    result = await db.execute(select(Api).where(Api.id == api_id))
    api = result.scalar_one_or_none()

    if not api:
        raise HTTPException(status_code=404, detail="API não encontrada")

    await db.delete(api)
    await db.commit()
    return {"message": "API deletada com sucesso!"}