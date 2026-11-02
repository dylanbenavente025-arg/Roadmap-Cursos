"""Reglas de la validación de aportes por el moderador (funciones puras).

Quién puede validar, desde qué estados y qué hace falta para rechazar
(BR-005). No consultan la base: el estado del aporte y el rol llegan por parámetro.
"""

from dataclasses import dataclass

from app.cursos.reglas import EstadoCurso, transicion_permitida
from app.excepciones import ErrorDeNegocio
from app.identidad.roles import Rol

LARGO_MAXIMO_MOTIVO = 500
ROLES_VALIDADORES = {Rol.MODERADOR}


@dataclass(frozen=True)
class Decision:
    """Lo que manda el moderador (BackendSchema §3.3: POST /aportes/{id}/validar)."""

    aprobado: bool
    motivo: str | None = None


@dataclass(frozen=True)
class ResultadoValidacion:
    estado: EstadoCurso
    motivo_rechazo: str | None


def puede_validar(rol: Rol) -> bool:
    return rol in ROLES_VALIDADORES


def decidir_validacion(
    estado_actual: EstadoCurso, rol: Rol, decision: Decision
) -> ResultadoValidacion:
    """Aplica la decisión del moderador y devuelve el nuevo estado del aporte.

    El orden de los controles importa: primero el permiso (para no revelarle a
    un usuario común en qué estado está un aporte), después el estado y al final
    los datos de la decisión.
    """
    if not puede_validar(rol):
        raise ErrorDeNegocio("PERMISO_DENEGADO", "Solo un moderador puede validar aportes")

    nuevo_estado = EstadoCurso.PUBLICADO if decision.aprobado else EstadoCurso.RECHAZADO
    if not transicion_permitida(estado_actual, nuevo_estado):
        raise ErrorDeNegocio("APORTE_YA_DECIDIDO", "Este aporte ya fue aprobado o rechazado")

    if decision.aprobado:
        return ResultadoValidacion(estado=nuevo_estado, motivo_rechazo=None)

    motivo = (decision.motivo or "").strip()
    if not motivo:
        raise ErrorDeNegocio(
            "MOTIVO_OBLIGATORIO", "Para rechazar hay que indicar el motivo", campo="motivo"
        )
    if len(motivo) > LARGO_MAXIMO_MOTIVO:
        raise ErrorDeNegocio(
            "MOTIVO_DEMASIADO_LARGO",
            f"El motivo no puede superar los {LARGO_MAXIMO_MOTIVO} caracteres",
            campo="motivo",
        )
    return ResultadoValidacion(estado=nuevo_estado, motivo_rechazo=motivo)