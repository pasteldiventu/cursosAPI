from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import Abrigos
from schemas.curso_schema import AbrigosSchema

from core.deps import get_session

router = APIRouter()


#post abrigo
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AbrigosSchema)
async def post_curso(abrigo: AbrigosSchema, db: AsyncSession = Depends(get_session)):
    novo_abrigo = Abrigos(titulo=abrigo.titulo, aulas=abrigo.aulas, horas=abrigo.horas)

    db.add(novo_abrigo)
    await db.commit()

    return novo_abrigo


#GET abrigos
@router.get('/', response_model=List[AbrigosSchema])
async def get_abrigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Abrigos)
        result = await session.execute(query)
        abrigos: List[Abrigos] = result.scalars().all()

        return abrigos
    

#get abrigo
@router.get('/{abrigo_id}',response_model=AbrigosSchema, status_code=status.HTTP_200_OK)
async def get_abrigo(abrigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Abrigos).filter(Abrigos.id == abrigo_id)
        result = await session.execute(query)
        abrigo = result.scalar_one_or_none()

        if abrigo:
            return abrigo
        else:
            raise HTTPException (detail='Abrigo não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


#put abrigo
@router.put('/{abrigo_id}',response_model=AbrigosSchema ,status_code=status.HTTP_202_ACCEPTED)
async def put_abrigo(abrigo_id: int, abrigo: AbrigosSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Abrigos).filter(Abrigos.id == abrigo_id)
        result = await session.execute(query)
        abrigo_up = result.scalar_one_or_none()

        if abrigo_up:
            abrigo_up.endereco = abrigo.endereco
            abrigo_up.telefone = abrigo.telefone

            await session.commit()
        else:
             raise HTTPException(status_code=404, detail="Name field is required")
        return(abrigo_up)
    

#delete abrigo
@router.delete('/{abrigo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_abrigo(abrigo_id: int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Abrigos).filter(Abrigos.id == abrigo_id)
        result = await session.execute(query)
        abrigo_del = result.scalar_one_or_none()

        if abrigo_del:
            await session.delete(abrigo_del)
            await session.commit()

            return Response(status_code=status.HTTP_200_OK)
        else:
            raise HTTPException (detail='Abrigo não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


