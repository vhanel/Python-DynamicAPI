from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.api_schema import ApiCreate, ApiUpdate
from controllers.api_controller import create_api, update_existing_api, delete_existing_api, list_apis
from database.api_database import get_session
from services.dynamic_loader import reload_dynamic_routes
from models.api_model import Api

router = APIRouter(prefix="/admin", tags=["Admin APIs"])

@router.get("/apis")
async def get_all_apis(db: AsyncSession = Depends(get_session)):
    apis = await list_apis(db)
    return apis

@router.post("/apis")
async def register_api(api: ApiCreate, db: AsyncSession = Depends(get_session)):
    new_api = await create_api(db, api)
    return {"message": "API criada com sucesso!", "id": new_api.id}

@router.put("/apis/{api_id}")
async def update_api(api_id: int, api: ApiUpdate, db: AsyncSession = Depends(get_session)):
    updated_api = await update_existing_api(db, api_id, api)
    return {"message": "API atualizada com sucesso!", "api": updated_api}

@router.delete("/apis/{api_id}")
async def delete_api(api_id: int, db: AsyncSession = Depends(get_session)):
    return await delete_existing_api(db, api_id)

@router.post("/reload-dynamic-routes")
async def reload_routes(session: AsyncSession = Depends(get_session)):
    from app.main import app  # evitar import circular
    result = await session.execute(select(Api))
    apis = result.scalars().all()
    await reload_dynamic_routes(app, apis)
    return {"message": "Dynamic routes reloaded successfully"}
