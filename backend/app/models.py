from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Text,
    ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class StatusAgendamento(str, enum.Enum):
    pendente = "pendente"
    confirmado = "confirmado"
    cancelado = "cancelado"
    concluido = "concluido"


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    telefone = Column(String(20), nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    agendamentos = relationship(
        "Agendamento", back_populates="cliente", cascade="all, delete-orphan"
    )


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    servico = Column(String(150), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    status = Column(
        SAEnum(StatusAgendamento, name="status_agendamento"),
        default=StatusAgendamento.pendente,
        nullable=False,
    )
    observacoes = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciona cada agendamento a exatamente um cliente.
    cliente = relationship("Cliente", back_populates="agendamentos")
