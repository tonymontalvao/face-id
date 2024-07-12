from fastapi import APIRouter, status, Depends, HTTPException, Response
from pydantic import BaseModel as SCBaseModel
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from core.database import get_session
from models.empresa_model import EmpresaModel


router = APIRouter()


class DBSchema(SCBaseModel):
    id: int
    componente: str
    confianca: float
    usuario: str
    senha: str
    amostras: int


# Chamadas
@router.post('/', response_model=DBSchema)
def post(params: DBSchema, db: Session = Depends(get_session)):
    with db as conn:
        query = select(EmpresaModel).filter(EmpresaModel.id == params.id)
        result: DBSchema = conn.execute(query).scalar_one_or_none()

        if result:
            if params.componente:
                result.componente = params.componente

            if params.confianca:
                result.confianca = params.confianca

            if params.usuario:
                result.usuario = params.usuario

            if params.senha:
                result.senha = params.senha

            if params.amostras:
                result.amostras = params.amostras

            conn.commit()

            return result
        else:
            register = EmpresaModel(
                id=params.id,
                componente=params.componente,
                confianca=params.confianca,
                usuario=params.usuario,
                senha=params.senha,
                amostras=params.amostras
            )

            db.add(register)
            db.commit()
            return register


@router.get('/{id}')
def get(id: int, db: Session = Depends(get_session)):
    with db as conn:
        query = select(EmpresaModel).filter(EmpresaModel.id == id)
        result: DBSchema = conn.execute(query).scalar_one_or_none()

        if result:
            return result
        else:
            raise HTTPException(detail='Registro não encontrado!',
                                status_code=status.HTTP_404_NOT_FOUND)
