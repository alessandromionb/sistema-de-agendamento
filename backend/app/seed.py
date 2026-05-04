from datetime import datetime, timedelta
from random import choice
from time import time_ns

from sqlalchemy.orm import Session

from app.models import Agendamento, Cliente, StatusAgendamento

NOMES = [
    "Lucas Almeida",
    "Beatriz Costa",
    "Rafael Nunes",
    "Camila Rocha",
    "Pedro Henrique",
    "Mariana Lima",
    "Gustavo Martins",
    "Larissa Ferreira",
    "Thiago Barbosa",
    "Patricia Gomes",
    "Felipe Carvalho",
    "Renata Araujo",
    "Bruno Ribeiro",
    "Leticia Moura",
    "Eduardo Castro",
    "Juliana Campos",
    "Carlos Mendes",
    "Amanda Vieira",
    "Vinicius Lopes",
    "Fernanda Dias",
]

SERVICOS = [
    "Consulta inicial",
    "Retorno de atendimento",
    "Avaliacao de servico",
    "Reuniao de acompanhamento",
    "Atendimento tecnico",
    "Orientacao personalizada",
    "Revisao de cadastro",
    "Confirmacao de dados",
]

STATUS = [
    StatusAgendamento.pendente,
    StatusAgendamento.confirmado,
    StatusAgendamento.cancelado,
    StatusAgendamento.concluido,
]


def seed_initial_data(db: Session) -> None:
    """Cria dados de demonstração apenas quando o banco está vazio."""
    if db.query(Cliente).first():
        return

    clientes = [
        Cliente(
            nome="Maria Oliveira",
            email="maria.oliveira@email.com",
            telefone="(63) 99991-1001",
        ),
        Cliente(
            nome="Joao Pereira",
            email="joao.pereira@email.com",
            telefone="(63) 99992-2002",
        ),
        Cliente(
            nome="Ana Souza",
            email="ana.souza@email.com",
            telefone="(63) 99993-3003",
        ),
    ]

    db.add_all(clientes)
    db.flush()

    agora = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    agendamentos = [
        Agendamento(
            cliente_id=clientes[0].id,
            servico="Consulta inicial",
            data_hora=agora + timedelta(days=1, hours=2),
            status=StatusAgendamento.pendente,
            observacoes="Primeiro contato com a cliente.",
        ),
        Agendamento(
            cliente_id=clientes[1].id,
            servico="Retorno de atendimento",
            data_hora=agora + timedelta(days=2, hours=4),
            status=StatusAgendamento.confirmado,
            observacoes="Confirmado por telefone.",
        ),
        Agendamento(
            cliente_id=clientes[2].id,
            servico="Avaliacao de servico",
            data_hora=agora + timedelta(days=4, hours=1),
            status=StatusAgendamento.pendente,
            observacoes=None,
        ),
        Agendamento(
            cliente_id=clientes[0].id,
            servico="Reagendamento",
            data_hora=agora + timedelta(days=7, hours=3),
            status=StatusAgendamento.cancelado,
            observacoes="Cliente solicitou nova data.",
        ),
    ]

    db.add_all(agendamentos)
    db.commit()


def seed_demo_data(db: Session, total_clientes: int, total_agendamentos: int) -> dict:
    lote = str(time_ns())[-5:]
    clientes = []

    for i in range(total_clientes):
        nome = NOMES[i % len(NOMES)]
        slug = nome.lower().replace(" ", ".")
        clientes.append(
            Cliente(
                nome=nome,
                email=f"{slug}{lote}{i}@email.com",
                telefone=f"(63) 9{9000 + i:04d}-{1000 + i:04d}",
            )
        )

    db.add_all(clientes)
    db.flush()

    agora = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    agendamentos = []
    for i in range(total_agendamentos):
        cliente = clientes[i % len(clientes)] if clientes else choice(db.query(Cliente).all())
        agendamentos.append(
            Agendamento(
                cliente_id=cliente.id,
                servico=SERVICOS[i % len(SERVICOS)],
                data_hora=agora + timedelta(days=(i % 14) + 1, hours=8 + (i % 8)),
                status=STATUS[i % len(STATUS)],
                observacoes=f"Registro demo criado no lote {lote}.",
            )
        )

    db.add_all(agendamentos)
    db.commit()

    return {
        "clientes_criados": len(clientes),
        "agendamentos_criados": len(agendamentos),
    }
