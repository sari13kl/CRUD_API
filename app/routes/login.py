from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario, UsuarioCriarAtualizar
from app.dependencies import get_usuario_repository

router = APIRouter(
    prefix='/login'
)

templates = Jinja2Templates(directory='templates')

@router.get('/', response_class=HTMLResponse)
async def pagina_login(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')

@router.post('/', response_class=HTMLResponse)
async def login(usuario_repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)], request: Request, email: Annotated[str, Form()], senha: Annotated[str, Form()]):
    usuario = await usuario_repository.obter_usuario_email_senha(email, senha)
    if usuario:
        response = RedirectResponse(url='/', status_code=303)
        response.set_cookie(key='session_token', value='token-senha', httponly=True)

        return response

    return templates.TemplateResponse(request=request, name='login.html', context={'email': email, 'senha': senha, 'error': 'Credenciais Inválidas'})
