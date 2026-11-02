"""Fixtures compartidas por los tests de integración.

Los tests de integración usan el PostgreSQL del docker-compose, en una base
aparte (aprovechaelbug_test) que se crea sola la primera vez. Cada test corre
dentro de una transacción que se deshace al terminar: los tests no se pisan
entre sí y la base queda siempre vacía.

Los tests unitarios no usan estas fixtures, así que corren sin base de datos.
"""

import os
from itertools import count

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.cursos.reglas import EstadoCurso, normalizar_url
from app.database import Base
from app.esquema import Categoria, Usuario, crear_tablas
from app.identidad.roles import Rol

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://aprovecha:cambiar@localhost:5432/aprovechaelbug_test",
)


def _crear_base_si_no_existe(url_texto: str) -> None:
    url = make_url(url_texto)
    admin = create_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
    with admin.connect() as conexion:
        existe = conexion.scalar(
            text("SELECT 1 FROM pg_database WHERE datname = :nombre"), {"nombre": url.database}
        )
        if not existe:
            conexion.execute(text(f'CREATE DATABASE "{url.database}"'))
    admin.dispose()


@pytest.fixture(scope="session")
def engine():
    """Una vez por ejecución: crea la base de test y sus tablas desde cero."""
    _crear_base_si_no_existe(TEST_DATABASE_URL)
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.drop_all(engine)
    crear_tablas(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine):
    """Una sesión por test, dentro de una transacción que se deshace al final."""
    with engine.connect() as conexion:
        transaccion = conexion.begin()
        session = Session(bind=conexion, join_transaction_mode="create_savepoint")
        yield session
        session.close()
        transaccion.rollback()


@pytest.fixture
def categorias(session) -> dict[str, Categoria]:
    programacion = Categoria(nombre="Programación")
    datos = Categoria(nombre="Datos")
    session.add_all([programacion, datos])
    session.flush()
    return {"programacion": programacion, "datos": datos}


@pytest.fixture
def autor(session) -> Usuario:
    usuario = Usuario(email="ana@ejemplo.com", nombre="Ana", password_hash="x")
    session.add(usuario)
    session.flush()
    return usuario


@pytest.fixture
def moderador(session) -> Usuario:
    usuario = Usuario(email="mod@ejemplo.com", nombre="Mod", password_hash="x", rol=Rol.MODERADOR)
    session.add(usuario)
    session.flush()
    return usuario


_numero = count(1)


@pytest.fixture
def datos_curso(categorias, autor, moderador):
    """Fábrica de datos de curso válidos; cada test cambia solo lo que le interesa."""

    def fabricar(**cambios) -> dict:
        n = next(_numero)
        datos = {
            "url": f"https://ejemplo.com/curso-{n}",
            "titulo": f"Curso {n}",
            "tema": "Programación",
            "version": "1.0",
            "anio_edicion": 2024,
            "docentes": "Ana Pérez",
            "tiene_cuestionarios": False,
            "requiere_examen": False,
            "extiende_certificado": True,
            "lo_tomo_aportante": True,
            "categoria_id": categorias["programacion"].id,
            "aportado_por": autor.id,
        }
        datos.update(cambios)
        datos.setdefault("url_normalizada", normalizar_url(datos["url"]))
        if datos.get("estado") == EstadoCurso.PUBLICADO:
            datos.setdefault("validado_por", moderador.id)
            datos.setdefault("validado_en", text("now()"))
        return datos

    return fabricar