"""Registro de todos los modelos y creación de las tablas.

Importar los modelos acá hace que Base.metadata conozca todas las tablas.
Mientras no haya migraciones con Alembic (tarea 0.4 del plan), las tablas se
crean con create_all al arrancar la API.
"""

from sqlalchemy import Engine

from app.categorias.models import Categoria
from app.cursos.models import Curso
from app.database import Base
from app.identidad.models import Usuario

__all__ = ["Categoria", "Curso", "Usuario", "crear_tablas"]


def crear_tablas(engine: Engine) -> None:
    Base.metadata.create_all(engine)