from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "agendamento"
    POSTGRES_PASSWORD: str = "20241si000"
    POSTGRES_DB: str = "agendamentos_db"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    LOKI_URL: str = "http://loki:3100"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"


settings = Settings()

engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Entrega uma sessão por requisição e fecha a conexão ao final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
