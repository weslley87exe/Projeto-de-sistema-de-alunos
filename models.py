from sqlalchemy import Column, Integer, String, Float
from database import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    nota = Column(Float, nullable=False)
    matricula = Column(String, unique=True, nullable=False)
