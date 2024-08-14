from sqlalchemy import Column, Integer, String, Text, DateTime
from core.configs import DBBaseModel


class FotosModel(DBBaseModel):
    __tablename__ = 'Fotos'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_pessoa: str = Column(Integer)
    idx_imagem: float = Column(String(100))
    hash_imagem: str = Column(Text)
    link_imagem: str = Column(String(500))
    dt_imagem: DateTime = Column(DateTime)
