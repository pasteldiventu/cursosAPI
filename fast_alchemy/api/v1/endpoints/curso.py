from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import Gatos
from schemas.curso_schema import GatosSchema

from core.deps import get_session

router = APIRouter()


#post gato
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=GatosSchema)
async def post_gato(gato: GatosSchema, db: AsyncSession = Depends(get_session)):
    novo_gato = Gatos(titulo=gato.titulo, aulas=gato.aulas, horas=gato.horas)

    db.add(novo_gato)
    await db.commit()

    return novo_gato



#GET gatos
@router.get('/', response_model=List[GatosSchema])
async def get_gatos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Gatos)
        result = await session.execute(query)
        gatos: List[Gatos] = result.scalars().all()

        return gatos
    

#get gato
@router.get('/{gato_id}',response_model=GatosSchema, status_code=status.HTTP_200_OK)
async def get_gato(gato_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Gatos).filter(Gatos.id == gato_id)
        result = await session.execute(query)
        gato = result.scalar_one_or_none()

        if gato:
            return gato
        else:
            raise HTTPException (detail='Gato não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


#put gato
@router.put('/{gato_id}',response_model=GatosSchema ,status_code=status.HTTP_202_ACCEPTED)
async def put_gato(gato_id: int, gato: GatosSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Gatos).filter(Gatos.id == gato_id)
        result = await session.execute(query)
        gato_up = result.scalar_one_or_none()

        if gato_up:
            gato_up.idade = gato.idade
            gato_up.detalhe = gato.detalhe

            await session.commit()
        else:
             raise HTTPException(status_code=404, detail="Name field is required")
        return(gato_up)
    

#delete gato
@router.delete('/{gato_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_gato(gato_id: int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Gatos).filter(Gatos.id == gato_id)
        result = await session.execute(query)
        gato_del = result.scalar_one_or_none()

        if gato_del:
            await session.delete(gato_del)
            await session.commit()

            return Response(status_code=status.HTTP_200_OK)
        else:
            raise HTTPException (detail='Gato não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


