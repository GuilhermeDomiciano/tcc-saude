from pydantic import BaseModel


class DimFonteRecursoCreate(BaseModel):
    codigo: str
    descricao: str


class DimFonteRecursoUpdate(BaseModel):
    codigo: str | None = None
    descricao: str | None = None


class DimFonteRecursoOut(BaseModel):
    id: int
    codigo: str
    descricao: str

