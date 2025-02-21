from fastapi import APIRouter

from api.v1.endpoints import curso, adotantes, adocao, abrigo


api_router = APIRouter()
api_router.include_router(curso.router, prefix='/gatos', tags=["gatos"])
api_router.include_router(adotantes.router, prefix='/abrigos', tags=["abrigos"])
api_router.include_router(adocao.router, prefix='/adocoes', tags=["adocoes"])
api_router.include_router(abrigo.router, prefix='/adotantes', tags=["adotantes"])