"""Tabla categorias: lista cerrada cargada por seed (BackendSchema §1.2)."""

from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), unique=True)