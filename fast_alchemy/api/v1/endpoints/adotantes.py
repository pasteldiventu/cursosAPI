from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import Adotantes
from schemas.curso_schema import AdotantesSchema

from core.deps import get_session

router = APIRouter()


#post adotante
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AdotantesSchema)
async def post_curso(adotante: AdotantesSchema, db: AsyncSession = Depends(get_session)):
    novo_adotante = Adotantes(titulo=adotante.titulo, aulas=adotante.aulas, horas=adotante.horas)

    db.add(novo_adotante)
    await db.commit()

    return novo_adotante


#GET adotantes
@router.get('/', response_model=List[AdotantesSchema])
async def get_adotantes(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Adotantes)
        result = await session.execute(query)
        adotantes: List[Adotantes] = result.scalars().all()

        return adotantes
    

#get adotante
@router.get('/{adotante_id}',response_model=AdotantesSchema, status_code=status.HTTP_200_OK)
async def get_adotante(adotante_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Adotantes).filter(Adotantes.id == adotante_id)
        result = await session.execute(query)
        adotante = result.scalar_one_or_none()

        if adotante:
            return adotante
        else:
            raise HTTPException (detail='Adotante não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


#put adotante
@router.put('/{adotante_id}',response_model=AdotantesSchema ,status_code=status.HTTP_202_ACCEPTED)
async def put_adotante(adotante_id: int, adotante: AdotantesSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Adotantes).filter(Adotantes.id == adotante_id)
        result = await session.execute(query)
        adotante_up = result.scalar_one_or_none()

        if adotante_up:
            adotante_up.telefone = adotante.telefone
            adotante_up.email = adotante.email
            adotante_up.endereco = adotante.endereco

            await session.commit()
        else:
             raise HTTPException(status_code=404, detail="Name field is required")
        return(adotante_up)
    

#delete adotante
@router.delete('/{adotante_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_adotante(adotante_id: int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Adotantes).filter(Adotantes.id == adotante_id)
        result = await session.execute(query)
        adotante_del = result.scalar_one_or_none()

        if adotante_del:
            await session.delete(adotante_del)
            await session.commit()

            return Response(status_code=status.HTTP_200_OK)
        else:
            raise HTTPException (detail='Adotante não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


