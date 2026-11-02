"""Datos iniciales (TRD TD-007): categorías, un usuario de la comunidad y cursos de ejemplo.

Es idempotente: si ya hay categorías, no hace nada. Así se puede ejecutar en
cada arranque sin duplicar datos.
"""

from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.cursos.reglas import EstadoCurso, normalizar_url
from app.esquema import Categoria, Curso, Usuario
from app.identidad.roles import Rol

CATEGORIAS = ["Datos", "Diseño", "Idiomas", "Infraestructura", "Programación"]

CURSOS_DE_EJEMPLO = [
    {
        "url": "https://learn.microsoft.com/training/",
        "titulo": "Fundamentos de la nube",
        "tema": "Cloud computing",
        "version": "2026",
        "anio_edicion": 2026,
        "docentes": "Equipo de Microsoft Learn",
        "categoria": "Infraestructura",
        "tiene_cuestionarios": True,
        "requiere_examen": False,
        "extiende_certificado": True,
        "aval_organizacion": "Microsoft",
        "lo_tomo_aportante": True,
    },
    {
        "url": "https://platzi.com/",
        "titulo": "Introducción a Python",
        "tema": "Programación",
        "version": "3.0",
        "anio_edicion": 2025,
        "docentes": "Equipo docente de Platzi",
        "categoria": "Programación",
        "tiene_cuestionarios": True,
        "requiere_examen": True,
        "extiende_certificado": False,
        "aval_organizacion": None,
        "lo_tomo_aportante": False,
    },
    {
        "url": "https://www.udemy.com/",
        "titulo": "Git desde cero",
        "tema": "Control de versiones",
        "version": "1.2",
        "anio_edicion": 2024,
        "docentes": "Docente invitado",
        "categoria": "Programación",
        "tiene_cuestionarios": False,
        "requiere_examen": False,
        "extiende_certificado": True,
        "aval_organizacion": None,
        "lo_tomo_aportante": True,
    },
]


def cargar_datos_iniciales(session: Session) -> None:
    if session.scalar(select(func.count()).select_from(Categoria)):
        return

    categorias = {nombre: Categoria(nombre=nombre) for nombre in CATEGORIAS}
    session.add_all(categorias.values())
    # Usuario que figura como autor y validador de los cursos de ejemplo.
    # "!" no es un hash bcrypt válido: nadie puede iniciar sesión con este usuario.
    comunidad = Usuario(
        email="comunidad@aprovechaelbug.local",
        nombre="Comunidad AprovechaElBug",
        password_hash="!",
        rol=Rol.MODERADOR,
    )
    session.add(comunidad)
    session.flush()

    ahora = datetime.now(UTC)
    for ejemplo in CURSOS_DE_EJEMPLO:
        datos = dict(ejemplo)
        categoria = categorias[datos.pop("categoria")]
        session.add(
            Curso(
                **datos,
                url_normalizada=normalizar_url(datos["url"]),
                categoria_id=categoria.id,
                aportado_por=comunidad.id,
                estado=EstadoCurso.PUBLICADO,
                validado_por=comunidad.id,
                validado_en=ahora,
            )
        )
    session.commit()