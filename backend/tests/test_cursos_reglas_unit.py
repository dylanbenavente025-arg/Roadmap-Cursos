"""Tests unitarios de las reglas de negocio del curso (ticket C27-T1).

Funciones puras: no usan base de datos ni HTTP, por eso corren en milisegundos.
Nombres: test_<funcion>_<escenario>_<esperado>. Cada test sigue el patrón AAA.
"""

from dataclasses import replace
from itertools import product

import pytest

from app.cursos.reglas import (
    DatosAporte,
    EstadoCurso,
    cambiar_estado,
    normalizar_url,
    transicion_permitida,
    validar_datos_aporte,
    verificar_url_disponible,
)
from app.excepciones import ErrorDeNegocio

ANIO_ACTUAL = 2026


def aporte_valido(**cambios) -> DatosAporte:
    """Un aporte completo y correcto; cada test cambia solo lo que quiere probar."""
    base = DatosAporte(
        url="https://www.ejemplo.com/cursos/python",
        categoria_id=1,
        titulo="Python desde cero",
        tema="Programación",
        version="2024",
        anio_edicion=2024,
        docentes="Ana Pérez",
        tiene_cuestionarios=True,
        requiere_examen=False,
        extiende_certificado=True,
        lo_tomo_aportante=True,
        aval_organizacion=None,
    )
    return replace(base, **cambios)


def codigos(errores) -> set[tuple[str, str]]:
    return {(e.campo, e.code) for e in errores}


# ---------- validar_datos_aporte ----------


def test_validar_datos_aporte_completo_sin_errores():
    # Arrange
    datos = aporte_valido()
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert errores == []


@pytest.mark.parametrize("campo", ["titulo", "tema", "version", "docentes", "url"])
def test_validar_datos_aporte_campo_vacio_campo_obligatorio(campo):
    # Arrange
    datos = aporte_valido(**{campo: "   "})
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert codigos(errores) == {(campo, "CAMPO_OBLIGATORIO")}


@pytest.mark.parametrize(
    ("campo", "limite"),
    [("titulo", 200), ("tema", 120), ("version", 50), ("docentes", 300), ("aval_organizacion", 150)],
)
def test_validar_datos_aporte_texto_supera_limite_texto_demasiado_largo(campo, limite):
    # Arrange
    datos = aporte_valido(**{campo: "x" * (limite + 1)})
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert codigos(errores) == {(campo, "TEXTO_DEMASIADO_LARGO")}


@pytest.mark.parametrize("campo", ["titulo", "aval_organizacion"])
def test_validar_datos_aporte_texto_en_el_limite_sin_errores(campo):
    # Arrange
    limite = {"titulo": 200, "aval_organizacion": 150}[campo]
    datos = aporte_valido(**{campo: "x" * limite})
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert errores == []


@pytest.mark.parametrize(
    "url",
    ["ftp://ejemplo.com/curso", "ejemplo.com/curso", "https://", "javascript:alert(1)"],
)
def test_validar_datos_aporte_url_sin_http_url_invalida(url):
    # Arrange
    datos = aporte_valido(url=url)
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert codigos(errores) == {("url", "URL_INVALIDA")}


def test_validar_datos_aporte_url_demasiado_larga_texto_demasiado_largo():
    # Arrange
    datos = aporte_valido(url="https://ejemplo.com/" + "a" * 2048)
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert codigos(errores) == {("url", "TEXTO_DEMASIADO_LARGO")}


def test_validar_datos_aporte_anio_futuro_anio_futuro():
    # Arrange
    datos = aporte_valido(anio_edicion=ANIO_ACTUAL + 1)
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert codigos(errores) == {("anio_edicion", "ANIO_FUTURO")}


def test_validar_datos_aporte_anio_actual_sin_errores():
    # Arrange
    datos = aporte_valido(anio_edicion=ANIO_ACTUAL)
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert errores == []


def test_validar_datos_aporte_anio_anterior_a_1990_anio_fuera_de_rango():
    # Arrange
    datos = aporte_valido(anio_edicion=1989)
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert codigos(errores) == {("anio_edicion", "ANIO_FUERA_DE_RANGO")}


def test_validar_datos_aporte_sin_declarar_si_lo_tomo_declaracion_obligatoria():
    # Arrange
    datos = aporte_valido(lo_tomo_aportante=None)
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert codigos(errores) == {("lo_tomo_aportante", "DECLARACION_OBLIGATORIA")}


def test_validar_datos_aporte_varios_errores_los_informa_todos():
    # Arrange
    datos = aporte_valido(titulo="", url="no-es-una-url", anio_edicion=ANIO_ACTUAL + 5)
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert codigos(errores) == {
        ("titulo", "CAMPO_OBLIGATORIO"),
        ("url", "URL_INVALIDA"),
        ("anio_edicion", "ANIO_FUTURO"),
    }


@pytest.mark.parametrize(
    ("cuestionarios", "examen", "certificado", "aval"),
    list(product([True, False], [True, False], [True, False], [None, "UTN"])),
)
def test_validar_datos_aporte_cualquier_combinacion_de_flags_sin_errores(cuestionarios, examen, certificado, aval):
    # Arrange
    datos = aporte_valido(
        tiene_cuestionarios=cuestionarios,
        requiere_examen=examen,
        extiende_certificado=certificado,
        aval_organizacion=aval,
    )
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert errores == []


def test_validar_datos_aporte_aval_vacio_sin_errores():
    # Arrange
    datos = aporte_valido(aval_organizacion="  ")
    # Act
    errores = validar_datos_aporte(datos, anio_actual=ANIO_ACTUAL)
    # Assert
    assert errores == []


# ---------- normalizar_url (BR-004) ----------


@pytest.mark.parametrize(
    ("original", "esperada"),
    [
        ("https://Ejemplo.com/Curso/?utm_source=a&id=3#x", "https://ejemplo.com/Curso?id=3"),
        ("HTTPS://EJEMPLO.COM/", "https://ejemplo.com"),
        ("https://ejemplo.com/curso?utm_medium=mail&utm_campaign=x", "https://ejemplo.com/curso"),
        ("  https://ejemplo.com/curso  ", "https://ejemplo.com/curso"),
        ("https://ejemplo.com/curso#modulo-2", "https://ejemplo.com/curso"),
        ("https://ejemplo.com/curso?b=2&a=1", "https://ejemplo.com/curso?b=2&a=1"),
    ],
)
def test_normalizar_url_variantes_misma_forma_canonica(original, esperada):
    # Arrange: los datos llegan por parámetro
    # Act
    resultado = normalizar_url(original)
    # Assert
    assert resultado == esperada


def test_normalizar_url_respeta_mayusculas_de_la_ruta():
    # Arrange
    url = "https://ejemplo.com/Curso/Python"
    # Act
    resultado = normalizar_url(url)
    # Assert
    assert resultado == "https://ejemplo.com/Curso/Python"


# ---------- verificar_url_disponible (BR-004) ----------


def test_verificar_url_disponible_url_nueva_devuelve_url_normalizada():
    # Arrange
    existentes = {"https://ejemplo.com/otro-curso"}
    # Act
    resultado = verificar_url_disponible("https://ejemplo.com/curso", existentes)
    # Assert
    assert resultado == "https://ejemplo.com/curso"


def test_verificar_url_disponible_url_repetida_con_otra_forma_url_duplicada():
    # Arrange
    existentes = {"https://ejemplo.com/curso"}
    # Act
    with pytest.raises(ErrorDeNegocio) as error:
        verificar_url_disponible("https://EJEMPLO.com/curso/?utm_source=x", existentes)
    # Assert
    assert error.value.code == "URL_DUPLICADA"


# ---------- transiciones de estado ----------


@pytest.mark.parametrize("nuevo", [EstadoCurso.PUBLICADO, EstadoCurso.RECHAZADO])
def test_transicion_permitida_desde_en_revision_true(nuevo):
    # Arrange
    actual = EstadoCurso.EN_REVISION
    # Act
    permitida = transicion_permitida(actual, nuevo)
    # Assert
    assert permitida is True


@pytest.mark.parametrize(
    ("actual", "nuevo"),
    [
        (EstadoCurso.PUBLICADO, EstadoCurso.RECHAZADO),
        (EstadoCurso.RECHAZADO, EstadoCurso.PUBLICADO),
        (EstadoCurso.PUBLICADO, EstadoCurso.EN_REVISION),
        (EstadoCurso.RECHAZADO, EstadoCurso.EN_REVISION),
        (EstadoCurso.EN_REVISION, EstadoCurso.EN_REVISION),
    ],
)
def test_transicion_permitida_desde_estado_final_o_mismo_estado_false(actual, nuevo):
    # Arrange: los estados llegan por parámetro
    # Act
    permitida = transicion_permitida(actual, nuevo)
    # Assert
    assert permitida is False


def test_cambiar_estado_transicion_valida_devuelve_nuevo_estado():
    # Arrange
    actual = EstadoCurso.EN_REVISION
    # Act
    nuevo = cambiar_estado(actual, EstadoCurso.PUBLICADO)
    # Assert
    assert nuevo == EstadoCurso.PUBLICADO


def test_cambiar_estado_desde_publicado_transicion_invalida():
    # Arrange
    actual = EstadoCurso.PUBLICADO
    # Act
    with pytest.raises(ErrorDeNegocio) as error:
        cambiar_estado(actual, EstadoCurso.RECHAZADO)
    # Assert
    assert error.value.code == "TRANSICION_INVALIDA"