"""Punto de entrada de la API de AprovechaElBug."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.cursos.router import router as cursos_router
from app.database import SessionLocal, engine
from app.errores import registrar_manejadores
from app.esquema import crear_tablas
from app.seed import cargar_datos_iniciales


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al arrancar: crea las tablas que falten y carga los datos iniciales.
    # En Docker Compose, el backend arranca recién cuando postgres está healthy (T10).
    crear_tablas(engine)
    with SessionLocal() as session:
        cargar_datos_iniciales(session)
    yield


app = FastAPI(title="AprovechaElBug API", version="0.1.0", lifespan=lifespan)

registrar_manejadores(app)
app.include_router(cursos_router)


@app.get("/health", tags=["infra"])
def health() -> dict[str, str]:
    return {"status": "ok"}