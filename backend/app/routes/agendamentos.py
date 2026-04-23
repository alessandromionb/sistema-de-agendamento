from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Agendamento, Cliente
from app.schemas.agendamento import AgendamentoCreate, AgendamentoOut, AgendamentoUpdate

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])


# ── GET /agendamentos ─────────────────────────────────────────
@router.get("/", response_model=list[AgendamentoOut])
def listar_agendamentos(
    skip: int = 0,
    limit: int = 100,
    cliente_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Agendamento)
    if cliente_id:
        query = query.filter(Agendamento.cliente_id == cliente_id)
    return query.offset(skip).limit(limit).all()


# ── GET /agendamentos/{id} ────────────────────────────────────
@router.get("/{agendamento_id}", response_model=AgendamentoOut)
def obter_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    ag = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return ag


# ── POST /agendamentos ────────────────────────────────────────
@router.post("/", response_model=AgendamentoOut, status_code=status.HTTP_201_CREATED)
def criar_agendamento(payload: AgendamentoCreate, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == payload.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    ag = Agendamento(**payload.model_dump())
    db.add(ag)
    db.commit()
    db.refresh(ag)
    return ag


# ── PUT /agendamentos/{id} ────────────────────────────────────
@router.put("/{agendamento_id}", response_model=AgendamentoOut)
def atualizar_agendamento(
    agendamento_id: int, payload: AgendamentoUpdate, db: Session = Depends(get_db)
):
    ag = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    dados = payload.model_dump(exclude_unset=True)
    for campo, valor in dados.items():
        setattr(ag, campo, valor)

    db.commit()
    db.refresh(ag)
    return ag


# ── DELETE /agendamentos/{id} ─────────────────────────────────
@router.delete("/{agendamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    ag = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    db.delete(ag)
    db.commit()