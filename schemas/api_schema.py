from pydantic import BaseModel
from typing import Optional

class ApiCreate(BaseModel):
    name: str
    endpoint: str
    sql_query: str
    tag: str
    is_active: bool = True

class ApiUpdate(BaseModel):
    name: Optional[str]
    endpoint: Optional[str]
    sql_query: Optional[str]
    tag: Optional[str]
    is_active: Optional[bool]