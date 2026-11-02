"""Tests de integración del CursoRepository (ticket C27-T4).

Corren contra PostgreSQL real (el del docker-compose): prueban que las consultas,
los filtros, los índices y las restricciones funcionan en el motor de verdad.
"""

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.cursos.reglas import EstadoCurso
from app.cursos.repository import CursoRepository


@pytest.fixture
def repo(session) -> CursoRepository:
    return CursoRepository(session)


@pytest.fixture
def tres_cursos(repo, datos_curso):
    """Tres cursos creados en orden: el último es el más reciente."""
    return [repo.create(**datos_curso()) for _ in range(3)]


# ---------- create + get_by_id ----------


def test_create_y_get_by_id_devuelve_el_curso_guardado(repo, session, datos_curso):
    # Arrange
    datos = datos_curso(titulo="Python desde cero")
    creado = repo.create(**datos)
    session.expunge_all()  # olvida los objetos en memoria: el get tiene que leer de la base
    # Act
    leido = repo.get_by_id(creado.id)
    # Assert
    assert (leido.id, leido.titulo, leido.url) == (creado.id, "Python desde cero", datos["url"])


def test_create_sin_estado_queda_en_revision(repo, datos_curso):
    # Arrange
    datos = datos_curso()
    # Act
    curso = repo.create(**datos)
    # Assert
    assert curso.estado == EstadoCurso.EN_REVISION


def test_get_by_id_inexistente_devuelve_none(repo):
    # Arrange
    id_inexistente = 999_999
    # Act
    curso = repo.get_by_id(id_inexistente)
    # Assert
    assert curso is None


def test_create_url_normalizada_repetida_integrity_error(repo, datos_curso):
    # Arrange: BR-004 también la garantiza la base, aunque dos pedidos lleguen a la vez
    repo.create(**datos_curso(url="https://ejemplo.com/python"))
    # Act / Assert
    with pytest.raises(IntegrityError):
        repo.create(**datos_curso(url="https://EJEMPLO.com/python/"))


def test_create_rechazado_sin_motivo_integrity_error(repo, datos_curso, moderador):
    # Arrange: el CHECK de la base es la red de seguridad de BR-005
    datos = datos_curso(
        estado=EstadoCurso.RECHAZADO, validado_por=moderador.id, validado_en=text("now()")
    )
    # Act / Assert
    with pytest.raises(IntegrityError):
        repo.create(**datos)


# ---------- listar: paginación ----------


def test_listar_primera_pagina_de_2_devuelve_2_items_y_total_3(repo, tres_cursos):
    # Arrange: tres cursos creados por la fixture
    # Act
    items, total = repo.listar(offset=0, limit=2)
    # Assert
    assert (len(items), total) == (2, 3)


def test_listar_segunda_pagina_devuelve_el_resto(repo, tres_cursos):
    # Arrange: tres cursos creados por la fixture
    # Act
    items, total = repo.listar(offset=2, limit=2)
    # Assert
    assert (len(items), total) == (1, 3)


def test_listar_pagina_fuera_de_rango_devuelve_lista_vacia_y_total(repo, tres_cursos):
    # Arrange: tres cursos creados por la fixture
    # Act
    items, total = repo.listar(offset=20, limit=20)
    # Assert
    assert (items, total) == ([], 3)


def test_listar_ordena_mas_recientes_primero(repo, tres_cursos):
    # Arrange
    ids_creacion = [c.id for c in tres_cursos]
    # Act
    items, _ = repo.listar(offset=0, limit=10)
    # Assert
    assert [c.id for c in items] == list(reversed(ids_creacion))


# ---------- listar: filtros ----------


def test_listar_por_estado_publicado_excluye_los_demas(repo, datos_curso):
    # Arrange
    publicado = repo.create(**datos_curso(estado=EstadoCurso.PUBLICADO))
    repo.create(**datos_curso())  # en revisión
    # Act
    items, total = repo.listar(offset=0, limit=10, estado=EstadoCurso.PUBLICADO)
    # Assert
    assert ([c.id for c in items], total) == ([publicado.id], 1)


def test_listar_q_parcial_sin_distinguir_mayusculas(repo, datos_curso):
    # Arrange
    python = repo.create(**datos_curso(titulo="Python desde cero"))
    repo.create(**datos_curso(titulo="Git avanzado"))
    # Act
    items, total = repo.listar(offset=0, limit=10, q="PYTH")
    # Assert
    assert ([c.id for c in items], total) == ([python.id], 1)


def test_listar_q_busca_tambien_en_el_tema(repo, datos_curso):
    # Arrange
    nube = repo.create(**datos_curso(titulo="Fundamentos", tema="Cloud computing"))
    repo.create(**datos_curso(titulo="Fundamentos", tema="Diseño"))
    # Act
    items, _ = repo.listar(offset=0, limit=10, q="cloud")
    # Assert
    assert [c.id for c in items] == [nube.id]


def test_listar_q_con_comodines_los_toma_como_texto(repo, datos_curso):
    # Arrange: en SQL, % y _ son comodines; el usuario los escribe como texto común
    porcentaje = repo.create(**datos_curso(titulo="SQL al 100% gratis"))
    repo.create(**datos_curso(titulo="SQL al 1000 gratis"))
    # Act
    items, _ = repo.listar(offset=0, limit=10, q="100%")
    # Assert
    assert [c.id for c in items] == [porcentaje.id]


def test_listar_q_vacio_no_filtra(repo, tres_cursos):
    # Arrange: tres cursos creados por la fixture
    # Act
    _, total = repo.listar(offset=0, limit=10, q="   ")
    # Assert
    assert total == 3


def test_listar_por_categoria(repo, datos_curso, categorias):
    # Arrange
    datos = repo.create(**datos_curso(categoria_id=categorias["datos"].id))
    repo.create(**datos_curso(categoria_id=categorias["programacion"].id))
    # Act
    items, total = repo.listar(offset=0, limit=10, categoria_id=categorias["datos"].id)
    # Assert
    assert ([c.id for c in items], total) == ([datos.id], 1)


def test_listar_q_y_categoria_combinados(repo, datos_curso, categorias):
    # Arrange
    buscado = repo.create(**datos_curso(titulo="Python para datos", categoria_id=categorias["datos"].id))
    repo.create(**datos_curso(titulo="Python web", categoria_id=categorias["programacion"].id))
    repo.create(**datos_curso(titulo="Estadística", categoria_id=categorias["datos"].id))
    # Act
    items, total = repo.listar(
        offset=0, limit=10, q="python", categoria_id=categorias["datos"].id
    )
    # Assert
    assert ([c.id for c in items], total) == ([buscado.id], 1)


def test_listar_trae_la_categoria_del_curso(repo, datos_curso, categorias):
    # Arrange
    repo.create(**datos_curso(categoria_id=categorias["datos"].id))
    # Act
    items, _ = repo.listar(offset=0, limit=10)
    # Assert
    assert items[0].categoria.nombre == "Datos"


# ---------- update ----------


def test_update_parcial_cambia_solo_los_campos_indicados(repo, session, datos_curso):
    # Arrange
    curso = repo.create(**datos_curso(titulo="Original", version="1.0"))
    # Act
    repo.update(curso.id, version="2.0")
    session.expunge_all()
    # Assert
    leido = repo.get_by_id(curso.id)
    assert (leido.titulo, leido.version) == ("Original", "2.0")


def test_update_inexistente_devuelve_none(repo):
    # Arrange
    id_inexistente = 999_999
    # Act
    resultado = repo.update(id_inexistente, titulo="X")
    # Assert
    assert resultado is None


def test_update_campo_inexistente_value_error(repo, datos_curso):
    # Arrange
    curso = repo.create(**datos_curso())
    # Act / Assert
    with pytest.raises(ValueError):
        repo.update(curso.id, campo_que_no_existe="X")


# ---------- delete ----------


def test_delete_y_get_by_id_devuelve_none(repo, datos_curso):
    # Arrange
    curso = repo.create(**datos_curso())
    # Act
    borrado = repo.delete(curso.id)
    # Assert
    assert (borrado, repo.get_by_id(curso.id)) == (True, None)


def test_delete_inexistente_devuelve_false(repo):
    # Arrange
    id_inexistente = 999_999
    # Act
    borrado = repo.delete(id_inexistente)
    # Assert
    assert borrado is False