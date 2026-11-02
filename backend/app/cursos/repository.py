"""Acceso a datos de cursos (TRD §3.1: la única puerta a la base para este dominio).

No tiene reglas de negocio (esas viven en app/cursos/reglas.py): solo guarda,
busca, actualiza y borra. Usa flush() y no commit(): confirmar la transacción
es decisión de quien lo llama.
"""

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.cursos.models import Curso
from app.cursos.reglas import EstadoCurso


def _escapar_like(texto: str) -> str:
    """En LIKE, % y _ son comodines: se escapan para buscarlos como texto común."""
    return texto.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


class CursoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, **campos) -> Curso:
        curso = Curso(**campos)
        self.session.add(curso)
        self.session.flush()
        return curso

    def get_by_id(self, curso_id: int) -> Curso | None:
        return self.session.get(Curso, curso_id)

    def listar(
        self,
        offset: int,
        limit: int,
        *,
        estado: EstadoCurso | None = None,
        q: str | None = None,
        categoria_id: int | None = None,
    ) -> tuple[list[Curso], int]:
        """Una página de cursos, los más recientes primero, y el total con los mismos filtros."""
        filtros = []
        if estado is not None:
            filtros.append(Curso.estado == estado)
        if categoria_id is not None:
            filtros.append(Curso.categoria_id == categoria_id)
        if q and q.strip():
            patron = f"%{_escapar_like(q.strip())}%"
            filtros.append(
                or_(Curso.titulo.ilike(patron, escape="\\"), Curso.tema.ilike(patron, escape="\\"))
            )

        total = self.session.scalar(select(func.count()).select_from(Curso).where(*filtros))
        consulta = (
            select(Curso)
            .where(*filtros)
            .order_by(Curso.creado_en.desc(), Curso.id.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(consulta)), total

    def update(self, curso_id: int, **campos) -> Curso | None:
        """Actualiza solo los campos indicados (actualización parcial)."""
        curso = self.get_by_id(curso_id)
        if curso is None:
            return None
        for campo, valor in campos.items():
            if campo not in Curso.__mapper__.columns:
                raise ValueError(f"El curso no tiene el campo '{campo}'")
            setattr(curso, campo, valor)
        self.session.flush()
        return curso

    def delete(self, curso_id: int) -> bool:
        curso = self.get_by_id(curso_id)
        if curso is None:
            return False
        self.session.delete(curso)
        self.session.flush()
        return True