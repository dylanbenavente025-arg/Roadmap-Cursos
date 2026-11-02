"""Conexión a PostgreSQL con SQLAlchemy (TRD §1)."""

from collections.abc import Iterator
from enum import StrEnum

from sqlalchemy import Enum, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import DATABASE_URL

# create_engine no abre ninguna conexión: la primera se abre al usarlo.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Base de todos los modelos: Base.metadata conoce todas las tablas."""


def enum_postgres(enum: type[StrEnum], nombre: str) -> Enum:
    """Tipo ENUM de PostgreSQL que guarda los valores ('en_revision'), no los nombres ('EN_REVISION')."""
    return Enum(enum, name=nombre, values_callable=lambda e: [m.value for m in e])


def get_session() -> Iterator[Session]:
    """Dependencia de FastAPI: una sesión por pedido, que se cierra al terminar."""
    with SessionLocal() as session:
        yield session