"""Configuración leída de variables de entorno (ver .env.example en la raíz)."""

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://aprovecha:cambiar@localhost:5432/aprovechaelbug",
)