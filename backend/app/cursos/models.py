"""Tabla cursos: un aporte es un curso en estado en_revision (BackendSchema §1.2)."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    SmallInteger,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.categorias.models import Categoria
from app.cursos.reglas import EstadoCurso
from app.database import Base, enum_postgres

PUBLICADO = text("estado = 'publicado'")


class Curso(Base):
    __tablename__ = "cursos"
    __table_args__ = (
        # Red de seguridad: la regla real del año (BR-012) vive en el service
        CheckConstraint("anio_edicion BETWEEN 1990 AND 2100", name="ck_cursos_anio_edicion"),
        # BR-005: un rechazo siempre tiene motivo
        CheckConstraint(
            "estado <> 'rechazado' OR motivo_rechazo IS NOT NULL", name="ck_cursos_motivo_rechazo"
        ),
        CheckConstraint(
            "estado = 'en_revision' OR (validado_por IS NOT NULL AND validado_en IS NOT NULL)",
            name="ck_cursos_validacion",
        ),
        # Índices parciales: solo indexan las filas que consulta cada pantalla
        Index("ix_cursos_publicados", text("creado_en DESC"), postgresql_where=PUBLICADO),
        Index(
            "ix_cursos_categoria_publicados",
            "categoria_id",
            text("creado_en DESC"),
            postgresql_where=PUBLICADO,
        ),
        Index(
            "ix_cursos_en_revision", "creado_en", postgresql_where=text("estado = 'en_revision'")
        ),
        Index("ix_cursos_aportado_por", "aportado_por", text("creado_en DESC")),
    )

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    url: Mapped[str] = mapped_column(String(2048))
    url_normalizada: Mapped[str] = mapped_column(String(2048), unique=True)  # BR-004
    titulo: Mapped[str] = mapped_column(String(200))
    tema: Mapped[str] = mapped_column(String(120))
    version: Mapped[str] = mapped_column(String(50))
    anio_edicion: Mapped[int] = mapped_column(SmallInteger)
    docentes: Mapped[str] = mapped_column(String(300))
    tiene_cuestionarios: Mapped[bool] = mapped_column(Boolean)
    requiere_examen: Mapped[bool] = mapped_column(Boolean)
    extiende_certificado: Mapped[bool] = mapped_column(Boolean)
    aval_organizacion: Mapped[str | None] = mapped_column(String(150))
    lo_tomo_aportante: Mapped[bool] = mapped_column(Boolean)  # BR-002
    estado: Mapped[EstadoCurso] = mapped_column(
        enum_postgres(EstadoCurso, "estado_curso"),
        default=EstadoCurso.EN_REVISION,
        server_default=EstadoCurso.EN_REVISION.value,
    )
    motivo_rechazo: Mapped[str | None] = mapped_column(String(500))
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    aportado_por: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    validado_por: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"))
    validado_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # La categoría se carga junto con el curso, en una sola consulta extra por listado
    categoria: Mapped[Categoria] = relationship(lazy="selectin")