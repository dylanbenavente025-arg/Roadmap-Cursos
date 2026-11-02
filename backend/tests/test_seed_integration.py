"""Tests de integración de los datos iniciales (TRD TD-007)."""

from sqlalchemy import func, select

from app.cursos.reglas import EstadoCurso
from app.esquema import Categoria, Curso
from app.seed import CATEGORIAS, CURSOS_DE_EJEMPLO, cargar_datos_iniciales


def test_cargar_datos_iniciales_crea_categorias_y_cursos_publicados(session):
    # Arrange: base vacía
    # Act
    cargar_datos_iniciales(session)
    # Assert
    estados = session.scalars(select(Curso.estado)).all()
    cantidad_categorias = session.scalar(select(func.count()).select_from(Categoria))
    assert (cantidad_categorias, estados) == (
        len(CATEGORIAS),
        [EstadoCurso.PUBLICADO] * len(CURSOS_DE_EJEMPLO),
    )


def test_cargar_datos_iniciales_dos_veces_no_duplica(session):
    # Arrange
    cargar_datos_iniciales(session)
    # Act
    cargar_datos_iniciales(session)
    # Assert
    assert session.scalar(select(func.count()).select_from(Curso)) == len(CURSOS_DE_EJEMPLO)