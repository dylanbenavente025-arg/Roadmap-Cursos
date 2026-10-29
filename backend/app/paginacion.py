"""Paginación por offset con total (TRD TD-002)."""

from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel


@dataclass
class ParametrosPaginacion:
    page: int
    page_size: int

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


def parametros_paginacion(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
) -> ParametrosPaginacion:
    return ParametrosPaginacion(page=page, page_size=page_size)


class Pagina[T](BaseModel):
    items: list[T]
    total: int
    page: int
    page_size: int