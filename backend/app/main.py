from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, SessionLocal, engine
from app.routes import clientes_router, agendamentos_router
from app.seed import seed_initial_data

# Para a atividade, criamos as tabelas na inicialização do container.
# Em produção, o caminho natural seria substituir isso por migrations.
Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    seed_initial_data(db)

app = FastAPI(
    title="Sistema de Agendamentos",
    description="API FastAPI para CRUD de clientes e agendamentos usando MySQL.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    root_path="/api",          # para que os docs funcionem via /api/docs
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes_router)
app.include_router(agendamentos_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "Sistema de Agendamentos"}
