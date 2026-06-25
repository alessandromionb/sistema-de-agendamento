from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request

from app.database import Base, SessionLocal, engine
from app.logger import send_loki_log
from app.routes import agendamentos_router, clientes_router, demo_router
from app.seed import seed_initial_data

# Para a atividade, criamos as tabelas na inicialização do container.
# Em produção, o caminho natural seria substituir isso por migrations.
try:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_initial_data(db)
except SQLAlchemyError as exc:
    send_loki_log(f"erro de conexao com PostgreSQL: {exc}", level="error")
    raise

app = FastAPI(
    title="Sistema de Agendamentos",
    description="API FastAPI para CRUD de clientes e agendamentos usando PostgreSQL.",
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
app.include_router(demo_router)


@app.on_event("startup")
def log_startup():
    send_loki_log("inicializacao da aplicacao FastAPI")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    send_loki_log(
        f"{request.method} {request.url.path} {response.status_code}",
        method=request.method,
        route=request.url.path,
        status_code=str(response.status_code),
    )
    return response


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "Sistema de Agendamentos"}
