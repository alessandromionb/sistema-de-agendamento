from datetime import datetime
from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    telefone: str | None = None


class ClienteOut(ClienteBase):
    id: int
    criado_em: datetime

    model_config = {"from_attributes": True}