# domain/jwt_models.py
from dataclasses import dataclass


@dataclass
class JwtRequest:
    login: str
    password: str


@dataclass
class JwtResponse:
    type: str
    accessToken: str
    refreshToken: str


@dataclass
class RefreshJwtRequest:
    refreshToken: str
