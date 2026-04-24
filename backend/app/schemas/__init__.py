"""
Schemas Pydantic — exportações centralizadas.
"""
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from app.schemas.agendamento import AgendamentoCreate, AgendamentoUpdate, AgendamentoOut
 
__all__ = [
    "ClienteCreate",
    "ClienteUpdate",
    "ClienteOut",
    "AgendamentoCreate",
    "AgendamentoUpdate",
    "AgendamentoOut",
]
 