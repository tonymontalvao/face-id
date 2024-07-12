from fastapi import APIRouter
from api.endpoints import empresa, imagem

api_router = APIRouter()

# empresas
api_router.include_router(
    empresa.router, prefix='/empresas', tags=["Empresas"])

# imagens
api_router.include_router(imagem.router, prefix='/imagens', tags=["Imagens"])
