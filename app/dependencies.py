from typing import Annotated
from fastapi import Depends

from app.db.local import BancodedadosLocal
from app.db.cliente_repository import ClienteRepository
from app.db.usuario_repository import UsuarioRepository

banco_de_dados = BancodedadosLocal()

def get_db() -> BancodedadosLocal:
    return banco_de_dados

def get_cliente_repository(banco_de_dados_local: Annotated[BancodedadosLocal, Depends(get_db)]) -> ClienteRepository:
    return ClienteRepository(banco_de_dados_local)

def get_usuario_repository(banco_de_dados_local: Annotated[BancodedadosLocal, Depends(get_db)]) -> UsuarioRepository:
    return UsuarioRepository(banco_de_dados_local)