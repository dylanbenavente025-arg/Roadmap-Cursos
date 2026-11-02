"""Tests unitarios de la validación de aportes por el moderador (ticket C27-T3).

Los tests comparan el `code` del error, nunca el texto: el código es parte del
contrato (lo usan el frontend y el handler HTTP) y el mensaje puede cambiar.
"""

import pytest

from app.aportes.reglas import (
    LARGO_MAXIMO_MOTIVO,
    Decision,
    ResultadoValidacion,
    decidir_validacion,
    puede_validar,
)
from app.cursos.reglas import EstadoCurso
from app.excepciones import ErrorDeNegocio
from app.identidad.roles import Rol

APROBAR = Decision(aprobado=True)


def rechazar(motivo: str | None) -> Decision:
    return Decision(aprobado=False, motivo=motivo)


# ---------- puede_validar ----------


def test_puede_validar_moderador_true():
    # Arrange
    rol = Rol.MODERADOR
    # Act
    permitido = puede_validar(rol)
    # Assert
    assert permitido is True


def test_puede_validar_usuario_comun_false():
    # Arrange
    rol = Rol.USUARIO
    # Act
    permitido = puede_validar(rol)
    # Assert
    assert permitido is False


# ---------- decidir_validacion: camino feliz ----------


def test_decidir_validacion_aprobar_aporte_en_revision_queda_publicado():
    # Arrange
    estado = EstadoCurso.EN_REVISION
    # Act
    resultado = decidir_validacion(estado, Rol.MODERADOR, APROBAR)
    # Assert
    assert resultado == ResultadoValidacion(estado=EstadoCurso.PUBLICADO, motivo_rechazo=None)


def test_decidir_validacion_rechazar_con_motivo_queda_rechazado_con_motivo():
    # Arrange
    decision = rechazar("El enlace lleva a un curso pago")
    # Act
    resultado = decidir_validacion(EstadoCurso.EN_REVISION, Rol.MODERADOR, decision)
    # Assert
    assert resultado == ResultadoValidacion(
        estado=EstadoCurso.RECHAZADO, motivo_rechazo="El enlace lleva a un curso pago"
    )


def test_decidir_validacion_rechazar_quita_espacios_del_motivo():
    # Arrange
    decision = rechazar("   Curso duplicado   ")
    # Act
    resultado = decidir_validacion(EstadoCurso.EN_REVISION, Rol.MODERADOR, decision)
    # Assert
    assert resultado.motivo_rechazo == "Curso duplicado"


def test_decidir_validacion_aprobar_con_motivo_ignora_el_motivo():
    # Arrange: el motivo solo tiene sentido al rechazar
    decision = Decision(aprobado=True, motivo="no debería guardarse")
    # Act
    resultado = decidir_validacion(EstadoCurso.EN_REVISION, Rol.MODERADOR, decision)
    # Assert
    assert resultado.motivo_rechazo is None


def test_decidir_validacion_motivo_en_el_limite_lo_acepta():
    # Arrange
    decision = rechazar("x" * LARGO_MAXIMO_MOTIVO)
    # Act
    resultado = decidir_validacion(EstadoCurso.EN_REVISION, Rol.MODERADOR, decision)
    # Assert
    assert resultado.estado == EstadoCurso.RECHAZADO


# ---------- decidir_validacion: permisos ----------


@pytest.mark.parametrize("decision", [APROBAR, Decision(aprobado=False, motivo="Motivo")])
def test_decidir_validacion_usuario_comun_permiso_denegado(decision):
    # Arrange
    rol = Rol.USUARIO
    # Act
    with pytest.raises(ErrorDeNegocio) as error:
        decidir_validacion(EstadoCurso.EN_REVISION, rol, decision)
    # Assert
    assert error.value.code == "PERMISO_DENEGADO"


def test_decidir_validacion_usuario_comun_sobre_aporte_ya_decidido_permiso_denegado():
    # Arrange: los permisos se revisan antes que el estado, para no revelar información
    estado = EstadoCurso.PUBLICADO
    # Act
    with pytest.raises(ErrorDeNegocio) as error:
        decidir_validacion(estado, Rol.USUARIO, APROBAR)
    # Assert
    assert error.value.code == "PERMISO_DENEGADO"


# ---------- decidir_validacion: estados admitidos ----------


@pytest.mark.parametrize("estado", [EstadoCurso.PUBLICADO, EstadoCurso.RECHAZADO])
@pytest.mark.parametrize("decision", [APROBAR, Decision(aprobado=False, motivo="Motivo")])
def test_decidir_validacion_aporte_ya_decidido_aporte_ya_decidido(estado, decision):
    # Arrange: publicado y rechazado son estados finales
    rol = Rol.MODERADOR
    # Act
    with pytest.raises(ErrorDeNegocio) as error:
        decidir_validacion(estado, rol, decision)
    # Assert
    assert error.value.code == "APORTE_YA_DECIDIDO"


# ---------- decidir_validacion: motivo del rechazo ----------


@pytest.mark.parametrize("motivo", [None, "", "    "])
def test_decidir_validacion_rechazar_sin_motivo_motivo_obligatorio(motivo):
    # Arrange
    decision = rechazar(motivo)
    # Act
    with pytest.raises(ErrorDeNegocio) as error:
        decidir_validacion(EstadoCurso.EN_REVISION, Rol.MODERADOR, decision)
    # Assert
    assert error.value.code == "MOTIVO_OBLIGATORIO"


def test_decidir_validacion_rechazar_sin_motivo_indica_el_campo():
    # Arrange
    decision = rechazar(None)
    # Act
    with pytest.raises(ErrorDeNegocio) as error:
        decidir_validacion(EstadoCurso.EN_REVISION, Rol.MODERADOR, decision)
    # Assert
    assert error.value.campo == "motivo"


def test_decidir_validacion_motivo_supera_limite_motivo_demasiado_largo():
    # Arrange
    decision = rechazar("x" * (LARGO_MAXIMO_MOTIVO + 1))
    # Act
    with pytest.raises(ErrorDeNegocio) as error:
        decidir_validacion(EstadoCurso.EN_REVISION, Rol.MODERADOR, decision)
    # Assert
    assert error.value.code == "MOTIVO_DEMASIADO_LARGO"