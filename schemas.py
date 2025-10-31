from pydantic import BaseModel

class AlunoBase(BaseModel):
    nome: str
    idade: int
    nota: str
    matricula: str


class AlunoCreate(AlunoBase):
    pass


class AlunoUpdate(AlunoBase):
    pass


class Aluno(AlunoBase):
    id: int

    class Config:
        orm_mode = True
