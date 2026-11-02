"""Reglas del roadmap personal (funciones puras: sin base de datos ni HTTP).

Cada función recibe los ítems del roadmap de UN usuario y devuelve una lista
nueva, sin modificar la original. El service de la Fase 2 carga los ítems de la
base, aplica la regla y guarda el resultado.
"""

from dataclasses import dataclass, replace
from enum import StrEnum

from app.cursos.reglas import EstadoCurso
from app.excepciones import ErrorDeNegocio


class EstadoAvance(StrEnum):
    PENDIENTE = "pendiente"
    EN_CURSO = "en_curso"
    COMPLETADO = "completado"


class Direccion(StrEnum):
    SUBIR = "subir"
    BAJAR = "bajar"


@dataclass(frozen=True)
class ItemRoadmap:
    curso_id: int
    orden: int
    estado_avance: EstadoAvance = EstadoAvance.PENDIENTE


def _ordenados(items: list[ItemRoadmap]) -> list[ItemRoadmap]:
    return sorted(items, key=lambda item: item.orden)


def _posicion(items: list[ItemRoadmap], curso_id: int) -> int:
    for posicion, item in enumerate(items):
        if item.curso_id == curso_id:
            return posicion
    raise ErrorDeNegocio("CURSO_NO_EN_ROADMAP", "Ese curso no está en tu roadmap")


def agregar_curso(
    items: list[ItemRoadmap], curso_id: int, estado_curso: EstadoCurso | None
) -> list[ItemRoadmap]:
    """Agrega el curso al final (BR-006 y BR-007).

    `estado_curso` es None si el curso no existe.
    """
    if estado_curso is None:
        raise ErrorDeNegocio("CURSO_NO_ENCONTRADO", "El curso no existe")
    if estado_curso != EstadoCurso.PUBLICADO:
        raise ErrorDeNegocio("CURSO_NO_PUBLICADO", "Solo se pueden agregar cursos publicados")
    if any(item.curso_id == curso_id for item in items):
        raise ErrorDeNegocio("CURSO_YA_INCLUIDO", "Ese curso ya está en tu roadmap")

    siguiente = max((item.orden for item in items), default=0) + 1
    return [*items, ItemRoadmap(curso_id=curso_id, orden=siguiente)]


def mover(items: list[ItemRoadmap], curso_id: int, direccion: Direccion) -> list[ItemRoadmap]:
    """Intercambia la posición del curso con su vecino (BackendSchema §3.4).

    En un extremo no cambia nada: subir el primero o bajar el último.
    """
    ordenados = _ordenados(items)
    posicion = _posicion(ordenados, curso_id)
    vecino = posicion - 1 if direccion == Direccion.SUBIR else posicion + 1
    if not 0 <= vecino < len(ordenados):
        return ordenados

    actual, otro = ordenados[posicion], ordenados[vecino]
    ordenados[posicion] = replace(actual, orden=otro.orden)
    ordenados[vecino] = replace(otro, orden=actual.orden)
    return _ordenados(ordenados)


def quitar(items: list[ItemRoadmap], curso_id: int) -> list[ItemRoadmap]:
    posicion = _posicion(items, curso_id)
    return items[:posicion] + items[posicion + 1 :]


def cambiar_avance(
    items: list[ItemRoadmap], curso_id: int, estado: EstadoAvance
) -> list[ItemRoadmap]:
    posicion = _posicion(items, curso_id)
    nuevos = list(items)
    nuevos[posicion] = replace(items[posicion], estado_avance=estado)
    return nuevos