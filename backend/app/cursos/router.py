"""Endpoints del catálogo comunitario (BackendSchema §3.2)."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.cursos.reglas import EstadoCurso
from app.cursos.repository import CursoRepository
from app.cursos.schemas import CursoOut
from app.database import get_session
from app.paginacion import Pagina, ParametrosPaginacion, parametros_paginacion

router = APIRouter(prefix="/api/v1/cursos", tags=["cursos"])


@router.get("", response_model=Pagina[CursoOut])
def listar_cursos(
    p: ParametrosPaginacion = Depends(parametros_paginacion),
    q: str | None = Query(None, max_length=100, description="Texto a buscar en título y tema"),
    categoria: int | None = Query(None, ge=1, description="Id de la categoría"),
    session: Session = Depends(get_session),
) -> Pagina[CursoOut]:
    # El catálogo muestra solo cursos publicados (BR-001)
    items, total = CursoRepository(session).listar(
        p.offset, p.page_size, estado=EstadoCurso.PUBLICADO, q=q, categoria_id=categoria
    )
    return Pagina[CursoOut](
        items=[CursoOut.model_validate(curso) for curso in items],
        total=total,
        page=p.page,
        page_size=p.page_size,
    )