"""Acceso a datos del catálogo.

SCAFFOLD: datos en memoria para que el frontend tenga qué mostrar.
Se reemplaza por consultas a PostgreSQL en las tareas 2.1, 2.2 y 2.4 del plan.
"""

from app.cursos.schemas import CursoOut

_CURSOS_PUBLICADOS = [
    CursoOut(
        id=1,
        url="https://learn.microsoft.com/training/",
        titulo="Fundamentos de la nube",
        tema="Cloud computing",
        version="2026",
        anio_edicion=2026,
        docentes="Equipo de Microsoft Learn",
        categoria={"id": 1, "nombre": "Infraestructura"},
        tiene_cuestionarios=True,
        requiere_examen=False,
        extiende_certificado=True,
        aval_organizacion="Microsoft",
        lo_tomo_aportante=True,
        estado="publicado",
    ),
    CursoOut(
        id=2,
        url="https://platzi.com/",
        titulo="Introducción a Python",
        tema="Programación",
        version="3.0",
        anio_edicion=2025,
        docentes="Equipo docente de Platzi",
        categoria={"id": 2, "nombre": "Programación"},
        tiene_cuestionarios=True,
        requiere_examen=True,
        extiende_certificado=False,
        aval_organizacion=None,
        lo_tomo_aportante=False,
        estado="publicado",
    ),
    CursoOut(
        id=3,
        url="https://www.udemy.com/",
        titulo="Git desde cero",
        tema="Control de versiones",
        version="1.2",
        anio_edicion=2024,
        docentes="Docente invitado",
        categoria={"id": 2, "nombre": "Programación"},
        tiene_cuestionarios=False,
        requiere_examen=False,
        extiende_certificado=True,
        aval_organizacion=None,
        lo_tomo_aportante=True,
        estado="publicado",
    ),
]


def listar_publicados(offset: int, limit: int) -> tuple[list[CursoOut], int]:
    return _CURSOS_PUBLICADOS[offset : offset + limit], len(_CURSOS_PUBLICADOS)