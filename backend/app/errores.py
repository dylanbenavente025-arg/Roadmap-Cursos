"""Formato uniforme de errores de la API (TRD TD-003).

Toda respuesta de error sale como:
{"error": {"code": "...", "message": "...", "details": [...]}}
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

CODIGOS = {
    401: "UNAUTHENTICATED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
    429: "RATE_LIMITED",
}


def respuesta_error(status: int, message: str, details: list | None = None) -> JSONResponse:
    cuerpo = {"code": CODIGOS.get(status, "INTERNAL_ERROR"), "message": message}
    if details:
        cuerpo["details"] = details
    return JSONResponse(status_code=status, content={"error": cuerpo})


def registrar_manejadores(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        mensaje = exc.detail if isinstance(exc.detail, str) else "Error"
        if exc.status_code == 404 and mensaje == "Not Found":
            mensaje = "Recurso no encontrado"
        return respuesta_error(exc.status_code, mensaje)

    @app.exception_handler(RequestValidationError)
    async def validacion(request: Request, exc: RequestValidationError) -> JSONResponse:
        details = [
            {"field": ".".join(str(p) for p in e["loc"][1:]), "message": e["msg"]}
            for e in exc.errors()
        ]
        return respuesta_error(422, "Hay campos inválidos", details)