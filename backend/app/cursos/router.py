"""Endpoints del catálogo comunitario (BackendSchema §3.2)."""

from fastapi import APIRouter, Depends

from app.cursos import repository
from app.cursos.schemas import CursoOut
from app.paginacion import Pagina, ParametrosPaginacion, parametros_paginacion

router = APIRouter(prefix="/api/v1/cursos", tags=["cursos"])


@router.get("", response_model=Pagina[CursoOut])
def listar_cursos(p: ParametrosPaginacion = Depends(parametros_paginacion)) -> Pagina[CursoOut]:
    items, total = repository.listar_publicados(offset=p.offset, limit=p.page_size)
    return Pagina[CursoOut](items=items, total=total, page=p.page, page_size=p.page_size)