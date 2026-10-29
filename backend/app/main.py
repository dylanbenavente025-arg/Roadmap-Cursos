"""Punto de entrada de la API de AprovechaElBug."""

from fastapi import FastAPI

from app.cursos.router import router as cursos_router
from app.errores import registrar_manejadores

app = FastAPI(title="AprovechaElBug API", version="0.1.0")

registrar_manejadores(app)
app.include_router(cursos_router)


@app.get("/health", tags=["infra"])
def health() -> dict[str, str]:
    return {"status": "ok"}