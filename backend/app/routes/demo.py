from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.seed import seed_demo_data

router = APIRouter(prefix="/demo", tags=["Demonstração"])


class PopularBancoPayload(BaseModel):
    clientes: int = Field(ge=1, le=100)
    agendamentos: int = Field(ge=0, le=200)


@router.post("/popular")
def popular_banco(payload: PopularBancoPayload, db: Session = Depends(get_db)):
    if payload.agendamentos and payload.clientes < 1:
        raise HTTPException(status_code=400, detail="Informe pelo menos um cliente.")

    return seed_demo_data(db, payload.clientes, payload.agendamentos)
