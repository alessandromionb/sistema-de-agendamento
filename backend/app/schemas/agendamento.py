from datetime import datetime
from pydantic import BaseModel
from app.models import StatusAgendamento


class AgendamentoBase(BaseModel):
    cliente_id: int
    servico: str
    data_hora: datetime
    status: StatusAgendamento = StatusAgendamento.pendente
    observacoes: str | None = None


class AgendamentoCreate(AgendamentoBase):
    pass


class AgendamentoUpdate(BaseModel):
    servico: str | None = None
    data_hora: datetime | None = None
    status: StatusAgendamento | None = None
    observacoes: str | None = None


class AgendamentoOut(AgendamentoBase):
    id: int
    criado_em: datetime

    model_config = {"from_attributes": True}