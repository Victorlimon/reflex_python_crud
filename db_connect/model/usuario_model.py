import reflex as rx 
from typing import Optional
from sqlmodel import Field

class usuario(rx.Model, table=True):
    id_usuario: Optional[int] = Field(default=None ,primary_key=True)
    correo: str 
    password: str