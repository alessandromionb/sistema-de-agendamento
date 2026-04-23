from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import clientes, agendamentos

# Cria as tabelas no banco na inicialização
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Agendamentos",
    description="API para gerenciamento de clientes e agendamentos",
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

app.include_router(clientes.router)
app.include_router(agendamentos.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "Sistema de Agendamentos"}