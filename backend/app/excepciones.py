"""Excepciones del dominio (TRD §4: las reglas lanzan errores de dominio).

`code` es estable: los tests, el frontend y el handler HTTP dependen de él.
`message` es para personas y puede cambiar sin romper nada.
"""


class ErrorDeNegocio(Exception):
    def __init__(self, code: str, message: str, campo: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.campo = campo