from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()

class TPais(Base):
    __tablename__ = "tpais"

    TenantId = Column(String(36), primary_key=True, index=True)
    PaisId = Column(String(36), primary_key=True, index=True)
    PaisNome = Column(String(100), nullable=False)
    PaisSigla = Column(String(20), nullable=False)

class TApiDyn(Base):
    __tablename__ = "tapidyn"

    ApiDynid = Column(String(36), primary_key=True, index=True)
    ApiDynName = Column(String(100), nullable=False)
    ApiDynEndpoint = Column(String(100), nullable=False)
    ApiDynSelect = Column(Text, nullable=False)
