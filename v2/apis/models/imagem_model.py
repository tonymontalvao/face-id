from core.configs import DBBaseModel
from sqlalchemy import Column, Integer, String, Text


class ImagemModel(DBBaseModel):
    __tablename__ = 'Imagens'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_empresa: int = Column(Integer)
    id_pessoa: int = Column(Integer)
    seq_amostra: int = Column(Integer)
    caminho_imagem: str = Column(String(254))
