from core.configs import settings
from sqlalchemy import Column,Integer,String

class Abrigos(settings.DBBaseModel):
    __tablename__='abrigos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    endereco: int = Column(String(255))
    telefone: int = Column(Integer)

class Adocoes(settings.DBBaseModel):
    __tablename__='adocoes'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_gato: int = Column(Integer)
    id_adotante: int = Column(Integer)
    data_adocao: int = Column(String(255))


class Adotantes(settings.DBBaseModel):
    __tablename__='adotantes'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    telefone: int = Column(Integer)
    email: str = Column(String(255))
    endereco: str = Column(String(255))
    

class Gatos(settings.DBBaseModel):
    __tablename__='gatos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(50))
    cor: str = Column(String(30))
    idade: int = Column(Integer)
    detalhe: str = Column(String(255))
    id_abrigo: int = Column(Integer)
    