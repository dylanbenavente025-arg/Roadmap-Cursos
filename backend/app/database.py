"""Conexión a PostgreSQL con SQLAlchemy (TRD §1).

En el scaffold solo se configura el engine: todavía no hay tablas ni consultas.
Las migraciones con Alembic llegan en la tarea 0.4 del Implementation Plan.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

# create_engine no abre ninguna conexión: la primera se abre al usarlo.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)