from typing import Optional
from pydantic import BaseModel as SCBaseModel


class AbrigosSchema(SCBaseModel):
    id: Optional[int]
    nome: str
    endereco: str
    telefone: int

class AdocoesSchema(SCBaseModel):
    id: Optional[int]
    id_gato: int
    id_adotante: int
    data_adocao: str


class AdotantesSchema(SCBaseModel):
    id: Optional[int]
    nome: str
    telefone: int
    email: str
    endereco: str

class GatosSchema(SCBaseModel):
    id: Optional[int]
    nome: str
    cor: str
    idade: int
    detalhes: str
    id_abrigo: int


class Config:
  orm_mode = True