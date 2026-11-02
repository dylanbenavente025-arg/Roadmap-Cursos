"""Contratos de salida del catálogo (BackendSchema §3.2)."""

from pydantic import BaseModel, ConfigDict


class CategoriaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str


class CursoOut(BaseModel):
    # from_attributes: se puede armar directo desde un objeto Curso de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: str
    titulo: str
    tema: str
    version: str
    anio_edicion: int
    docentes: str
    categoria: CategoriaOut
    tiene_cuestionarios: bool
    requiere_examen: bool
    extiende_certificado: bool
    aval_organizacion: str | None
    lo_tomo_aportante: bool
    estado: str
    en_mi_roadmap: bool = False