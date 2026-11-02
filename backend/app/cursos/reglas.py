"""Reglas de negocio del curso (funciones puras: sin base de datos ni HTTP).

Las usan el servicio de aportes y el de validación. Al no depender de nada
externo, se prueban con tests unitarios rápidos (tests/test_cursos_reglas_unit.py).
"""

from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from app.excepciones import ErrorDeNegocio

ANIO_MINIMO = 1990
LARGO_MAXIMO_URL = 2048
LARGOS_MAXIMOS = {
    "titulo": 200,
    "tema": 120,
    "version": 50,
    "docentes": 300,
}
LARGO_MAXIMO_AVAL = 150


class EstadoCurso(StrEnum):
    """Estados del ciclo de vida del curso (BackendSchema §2)."""

    EN_REVISION = "en_revision"
    PUBLICADO = "publicado"
    RECHAZADO = "rechazado"


# Desde cada estado, a qué estados se puede pasar. Publicado y rechazado son finales.
TRANSICIONES: dict[EstadoCurso, set[EstadoCurso]] = {
    EstadoCurso.EN_REVISION: {EstadoCurso.PUBLICADO, EstadoCurso.RECHAZADO},
    EstadoCurso.PUBLICADO: set(),
    EstadoCurso.RECHAZADO: set(),
}


@dataclass(frozen=True)
class DatosAporte:
    """Lo que manda el formulario de aporte (BackendSchema §3.3)."""

    url: str
    categoria_id: int
    titulo: str
    tema: str
    version: str
    anio_edicion: int
    docentes: str
    tiene_cuestionarios: bool
    requiere_examen: bool
    extiende_certificado: bool
    lo_tomo_aportante: bool | None
    aval_organizacion: str | None = None


@dataclass(frozen=True)
class ErrorCampo:
    campo: str
    code: str


def _es_url_http(url: str) -> bool:
    partes = urlsplit(url)
    return partes.scheme.lower() in {"http", "https"} and bool(partes.netloc)


def validar_datos_aporte(datos: DatosAporte, anio_actual: int) -> list[ErrorCampo]:
    """Devuelve todos los errores juntos, para marcar cada campo en el formulario.

    El año actual llega por parámetro (no se lee el reloj adentro) para que la
    función sea pura y el test pueda fijarlo.
    """
    errores: list[ErrorCampo] = []

    url = datos.url.strip()
    if not url:
        errores.append(ErrorCampo("url", "CAMPO_OBLIGATORIO"))
    elif len(url) > LARGO_MAXIMO_URL:
        errores.append(ErrorCampo("url", "TEXTO_DEMASIADO_LARGO"))
    elif not _es_url_http(url):
        errores.append(ErrorCampo("url", "URL_INVALIDA"))

    for campo, largo_maximo in LARGOS_MAXIMOS.items():
        valor = getattr(datos, campo).strip()
        if not valor:
            errores.append(ErrorCampo(campo, "CAMPO_OBLIGATORIO"))
        elif len(valor) > largo_maximo:
            errores.append(ErrorCampo(campo, "TEXTO_DEMASIADO_LARGO"))

    aval = (datos.aval_organizacion or "").strip()
    if len(aval) > LARGO_MAXIMO_AVAL:
        errores.append(ErrorCampo("aval_organizacion", "TEXTO_DEMASIADO_LARGO"))

    if datos.anio_edicion < ANIO_MINIMO:
        errores.append(ErrorCampo("anio_edicion", "ANIO_FUERA_DE_RANGO"))
    elif datos.anio_edicion > anio_actual:
        errores.append(ErrorCampo("anio_edicion", "ANIO_FUTURO"))

    if datos.lo_tomo_aportante is None:
        errores.append(ErrorCampo("lo_tomo_aportante", "DECLARACION_OBLIGATORIA"))

    return errores


def normalizar_url(url: str) -> str:
    """Forma canónica del enlace para detectar duplicados (BR-004).

    Esquema y host en minúsculas, sin fragmento, sin barra final y sin
    parámetros utm_*. La ruta conserva sus mayúsculas: en muchos sitios importan.
    """
    partes = urlsplit(url.strip())
    parametros = [
        (clave, valor)
        for clave, valor in parse_qsl(partes.query, keep_blank_values=True)
        if not clave.lower().startswith("utm_")
    ]
    return urlunsplit(
        (
            partes.scheme.lower(),
            partes.netloc.lower(),
            partes.path.rstrip("/"),
            urlencode(parametros),
            "",
        )
    )


def verificar_url_disponible(url: str, urls_existentes: set[str]) -> str:
    """Devuelve la URL normalizada o lanza URL_DUPLICADA si ya existe (en cualquier estado)."""
    normalizada = normalizar_url(url)
    if normalizada in urls_existentes:
        raise ErrorDeNegocio("URL_DUPLICADA", "Este curso ya fue aportado", campo="url")
    return normalizada


def transicion_permitida(actual: EstadoCurso, nuevo: EstadoCurso) -> bool:
    return nuevo in TRANSICIONES[actual]


def cambiar_estado(actual: EstadoCurso, nuevo: EstadoCurso) -> EstadoCurso:
    if not transicion_permitida(actual, nuevo):
        raise ErrorDeNegocio(
            "TRANSICION_INVALIDA",
            f"No se puede pasar de {actual} a {nuevo}",
        )
    return nuevo