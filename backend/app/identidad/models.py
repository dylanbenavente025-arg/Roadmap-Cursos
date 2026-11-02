"""Tabla usuarios (BackendSchema §1.2)."""

from datetime import datetime

from sqlalchemy import DateTime, Identity, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, enum_postgres
from app.identidad.roles import Rol


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    email: Mapped[str] = mapped_column(String(254))
    password_hash: Mapped[str] = mapped_column(String(100))
    nombre: Mapped[str] = mapped_column(String(100))
    rol: Mapped[Rol] = mapped_column(
        enum_postgres(Rol, "rol_usuario"), default=Rol.USUARIO, server_default=Rol.USUARIO.value
    )
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# El email es único sin distinguir mayúsculas (BR-011)
Index("ux_usuarios_email_lower", func.lower(Usuario.email), unique=True)