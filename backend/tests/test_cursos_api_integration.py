"""Tests de integración de la capa HTTP del catálogo (ticket C27-T4).

Prueban el endpoint completo (router → repository → PostgreSQL) con el
TestClient de FastAPI. La sesión de la app se reemplaza por la sesión del test,
así todo corre dentro de la transacción que se deshace al terminar.
"""

import pytest
from fastapi.testclient import TestClient

from app.cursos.reglas import EstadoCurso
from app.cursos.repository import CursoRepository
from app.database import get_session
from app.main import app


@pytest.fixture
def cliente(session):
    app.dependency_overrides[get_session] = lambda: session
    # Sin "with": no se ejecuta el lifespan, así el test no toca la base de desarrollo
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def repo(session) -> CursoRepository:
    return CursoRepository(session)


def test_health_responde_ok(cliente):
    # Arrange: la app con la sesión de test
    # Act
    respuesta = cliente.get("/health")
    # Assert
    assert (respuesta.status_code, respuesta.json()) == (200, {"status": "ok"})


def test_get_cursos_solo_publicados(cliente, repo, datos_curso):
    # Arrange
    publicado = repo.create(**datos_curso(estado=EstadoCurso.PUBLICADO))
    repo.create(**datos_curso())  # en revisión: no se ve en el catálogo (BR-001)
    # Act
    cuerpo = cliente.get("/api/v1/cursos").json()
    # Assert
    assert ([c["id"] for c in cuerpo["items"]], cuerpo["total"]) == ([publicado.id], 1)


def test_get_cursos_paginado_respeta_page_y_page_size(cliente, repo, datos_curso):
    # Arrange
    for _ in range(3):
        repo.create(**datos_curso(estado=EstadoCurso.PUBLICADO))
    # Act
    cuerpo = cliente.get("/api/v1/cursos", params={"page": 2, "page_size": 2}).json()
    # Assert
    assert (len(cuerpo["items"]), cuerpo["total"], cuerpo["page"], cuerpo["page_size"]) == (1, 3, 2, 2)


def test_get_cursos_incluye_la_categoria(cliente, repo, datos_curso, categorias):
    # Arrange
    repo.create(**datos_curso(estado=EstadoCurso.PUBLICADO, categoria_id=categorias["datos"].id))
    # Act
    curso = cliente.get("/api/v1/cursos").json()["items"][0]
    # Assert
    assert curso["categoria"] == {"id": categorias["datos"].id, "nombre": "Datos"}


def test_get_cursos_filtra_por_q_y_categoria(cliente, repo, datos_curso, categorias):
    # Arrange
    buscado = repo.create(
        **datos_curso(
            estado=EstadoCurso.PUBLICADO, titulo="Python para datos", categoria_id=categorias["datos"].id
        )
    )
    repo.create(**datos_curso(estado=EstadoCurso.PUBLICADO, titulo="Python web"))
    # Act
    cuerpo = cliente.get(
        "/api/v1/cursos", params={"q": "python", "categoria": categorias["datos"].id}
    ).json()
    # Assert
    assert [c["id"] for c in cuerpo["items"]] == [buscado.id]


def test_get_cursos_page_size_mayor_a_50_validation_error(cliente):
    # Arrange: el máximo de page_size es 50 (TRD TD-002)
    # Act
    respuesta = cliente.get("/api/v1/cursos", params={"page_size": 51})
    # Assert
    error = respuesta.json()["error"]
    assert (respuesta.status_code, error["code"], error["details"][0]["field"]) == (
        422,
        "VALIDATION_ERROR",
        "page_size",
    )


def test_ruta_inexistente_not_found_con_formato_de_error(cliente):
    # Arrange: el formato de errores del TRD TD-003 también aplica a los 404
    # Act
    respuesta = cliente.get("/api/v1/no-existe")
    # Assert
    assert (respuesta.status_code, respuesta.json()["error"]["code"]) == (404, "NOT_FOUND")