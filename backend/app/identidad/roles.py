"""Roles de usuario (SPEC §8, vacío 2: usuario y moderador)."""

from enum import StrEnum


class Rol(StrEnum):
    USUARIO = "usuario"
    MODERADOR = "moderador"