from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import Adocoes
from schemas.curso_schema import AdocoesSchema

from core.deps import get_session

router = APIRouter()


#post adocao
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AdocoesSchema)
async def post_curso(adocao: AdocoesSchema, db: AsyncSession = Depends(get_session)):
    novo_adocao = Adocoes(titulo=adocao.titulo, aulas=adocao.aulas, horas=adocao.horas)

    db.add(novo_adocao)
    await db.commit()

    return novo_adocao


#GET adocoes
@router.get('/', response_model=List[AdocoesSchema])
async def get_adocoes(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Adocoes)
        result = await session.execute(query)
        adocoes: List[Adocoes] = result.scalars().all()

        return adocoes
    

#get adocao
@router.get('/{adocao_id}',response_model=AdocoesSchema, status_code=status.HTTP_200_OK)
async def get_adocao(adocao_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Adocoes).filter(Adocoes.id == adocao_id)
        result = await session.execute(query)
        adocao = result.scalar_one_or_none()

        if adocao:
            return adocao
        else:
            raise HTTPException (detail='Adocao não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


#put adocao
@router.put('/{adocao_id}',response_model=AdocoesSchema ,status_code=status.HTTP_202_ACCEPTED)
async def put_adocao(adocao_id: int, adocao: AdocoesSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Adocoes).filter(Adocoes.id == adocao_id)
        result = await session.execute(query)
        adocao_up = result.scalar_one_or_none()

        if adocao_up:
            adocao_up.data_adocao = adocao.data_adocao

            await session.commit()
        else:
             raise HTTPException(status_code=404, detail="Name field is required")
        return(adocao_up)
    

#delete adocao
@router.delete('/{adocao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_adocao(adocao_id: int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Adocoes).filter(Adocoes.id == adocao_id)
        result = await session.execute(query)
        adocao_del = result.scalar_one_or_none()

        if adocao_del:
            await session.delete(adocao_del)
            await session.commit()

            return Response(status_code=status.HTTP_200_OK)
        else:
            raise HTTPException (detail='Adocao não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


