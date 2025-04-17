""" 
from fastapi import APIRouter, Depends
from app.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from app.services.dynamic_loader import reload_dynamic_routes

router = APIRouter()

@router.post("/reload-dynamic-routes", tags=["Admin"])
async def reload_routes(session: AsyncSession = Depends(get_session)):
    from app.main import app  # evitar import circular
    await reload_dynamic_routes(app, session)
    return {"message": "Dynamic routes reloaded successfully"}
    
 """