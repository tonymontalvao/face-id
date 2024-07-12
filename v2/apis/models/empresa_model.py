from sqlalchemy import Column, Integer, String, Float
from core.configs import DBBaseModel


class EmpresaModel(DBBaseModel):
    __tablename__ = 'Empresas'
    id: int = Column(Integer, primary_key=True, autoincrement=False)
    componente: str = Column(String(100))
    confianca: float = Column(Float())
    usuario: str = Column(String(100))
    senha: str = Column(String(100))
    amostras: int = Column(Integer)
