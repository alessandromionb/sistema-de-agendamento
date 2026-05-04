from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import Agendamento, Cliente, StatusAgendamento


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
