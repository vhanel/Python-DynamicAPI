import asyncio
import hashlib
import json

from typing import Dict
from sqlalchemy.future import select
from services.dynamic_loader import reload_dynamic_routes
from database.api_database import get_session
from models.api_model import Api


class DynamicRouteMonitor:
    def __init__(self, app, interval: int = 60):
        self.app = app
        self.interval = interval
        self._cache: Dict[str, str] = {}

    @staticmethod
    def apis_hash(apis):
        data = sorted([{
            "endpoint": api.endpoint,
            "sql_query": api.sql_query,
            "name": api.name,
            "tag": api.tag
        } for api in apis], key=lambda x: x["endpoint"])
        return hashlib.md5(json.dumps(data).encode()).hexdigest()

    async def run(self):
        while True:
            async for session in get_session():
                result = await session.execute(select(Api))
                apis = result.scalars().all()

                #current = {api.endpoint: api.sql_query for api in apis}
                current_hash = self.apis_hash(apis)

                if current_hash != self._cache:
                    self._cache = current_hash
                    await reload_dynamic_routes(self.app, apis)

            await asyncio.sleep(self.interval)

