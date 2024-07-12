import os
import base64
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from pydantic import BaseModel as SCBaseModel
from core.database import get_session
from models.imagem_model import ImagemModel


router = APIRouter()

path_imagens = 'imagens'


class DBSchema(SCBaseModel):
    id_empresa: int
    id_pessoa: int
    seq_amostra: int
    caminho_imagem: str


class ApiSchemaAll(SCBaseModel):
    imagens: List[str]


@router.post('/{id_empresa}/{id_pessoa}')
def post(id_empresa: int, id_pessoa: int, params: ApiSchemaAll, db: Session = Depends(get_session)):
    with db as conn:
        # Busca imagens
        query = select(ImagemModel).where(
            ImagemModel.id_empresa == id_empresa, ImagemModel.id_pessoa == id_pessoa)

        results: List[DBSchema] = conn.scalars(query).all()

        # Deleta imagens
        if results:
            for result in results:
                print(result)
                conn.delete(result)
                conn.commit()

                if os.path.isfile(result.caminho_imagem):
                    os.remove(result.caminho_imagem)

        # Salva novas imagens
        amostra = 0

        path_empresa = f'{path_imagens}/{id_empresa}'
        if not os.path.isdir(path_empresa):
            os.mkdir(path_empresa)

        for param in params.imagens:
            amostra += 1
            caminhoImagem = (
                f'{path_empresa}/p.{id_pessoa}.{amostra}.jpg')

            with open(caminhoImagem, "wb") as file:
                file.write(base64.b64decode(param))

            register = ImagemModel(
                id_empresa=id_empresa,
                id_pessoa=id_pessoa,
                seq_amostra=amostra,
                caminho_imagem=caminhoImagem
            )

            db.add(register)
            db.commit()

        # Busca imagens
        query = select(ImagemModel).where(
            ImagemModel.id_empresa == id_empresa, ImagemModel.id_pessoa == id_pessoa)

        results: List[DBSchema] = conn.scalars(query).all()

        return results


@router.get('/{id_empresa}')
def get(id_empresa: int, db: Session = Depends(get_session)):
    with db as conn:
        # Busca imagens
        query = select(ImagemModel).where(
            ImagemModel.id_empresa == id_empresa)

        results: List[DBSchema] = conn.scalars(query).all()

        list = {'imagens': []}
        for result in results:
            if os.path.isfile(result.caminho_imagem):
                with open(result.caminho_imagem, "rb") as file:
                    encoded = base64.b64encode(file.read())
                    list['imagens'].append(
                        {'id_pessoa': result.id_pessoa, 'seq': result.seq_amostra, 'b64': encoded})
            else:
                conn.delete(result)
                conn.commit()

        if list:
            return list
        else:
            raise HTTPException(detail='Registro não encontrado!',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.get('/{id_empresa}/{id_pessoa}')
def get(id_empresa: int, id_pessoa: int, db: Session = Depends(get_session)):
    with db as conn:
        query = select(ImagemModel).where(
            ImagemModel.id_empresa == id_empresa, ImagemModel.id_pessoa == id_pessoa)

        results: List[DBSchema] = conn.scalars(query).all()

        list = {'imagens': []}
        for result in results:
            with open(result.caminho_imagem, "rb") as file:
                encoded = base64.b64encode(file.read())
                list['imagens'].append(encoded)

        if list:
            return list
        else:
            raise HTTPException(detail='Registro não encontrado!',
                                status_code=status.HTTP_404_NOT_FOUND)
