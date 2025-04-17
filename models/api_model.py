from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Api(Base):
    __tablename__ = "apis"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    endpoint = Column(String(200), unique=True, nullable=False)
    sql_query = Column(Text, nullable=False)
    tag = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
