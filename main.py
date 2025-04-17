import asyncio
import logging

from fastapi import FastAPI

from services.dynamic_monitor import DynamicRouteMonitor
from routers import api_routes

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app.include_router(api_routes.router)

monitor = DynamicRouteMonitor(app)

@app.on_event("startup")
async def startup():
    asyncio.create_task(monitor.run())  # inicia o monitoramento paralelo
