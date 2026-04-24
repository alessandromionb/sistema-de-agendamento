"""
Routers FastAPI — exportações centralizadas.
Cada router é incluído em app/main.py via app.include_router().
"""
from app.routes.clientes import router as clientes_router
from app.routes.agendamentos import router as agendamentos_router
 
__all__ = [
    "clientes_router",
    "agendamentos_router",
]
 