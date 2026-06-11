from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario, UsuarioCriarAtualizar
from app.dependencies import get_usuario_repository

router = APIRouter(
    prefix='/registro'
)

templates = Jinja2Templates(directory='templates')

@router.get('/', response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(request=request, name='registro.html')

@router.post('/')
async def registrar_usuario(
    request: Request, 
    usuario: Annotated[UsuarioRepository, 
    Depends(get_usuario_repository)], 
    nome: Annotated[str, Form()], 
    email: Annotated[str, Form()], 
    senha: Annotated[str, Form()], 
    confirma_senha: Annotated[str, Form()]
):
    data = {
        'nome': nome,
        'email': email,
        'senha': senha,
        'confirma_senha': confirma_senha
    }

    if not all([email, senha, nome, confirma_senha]):
        return templates.TemplateResponse(request=request, name='registro.html', context={'error': 'Campos Obrigatórios Faltantes', **data})

    usuario_existente = await usuario.obter_usuario_email(email)
    if usuario_existente:
        return templates.TemplateResponse(request=request, name='registro.html', context={'error': 'Usuário Invalido!', **data})
    
    usuario_criar = UsuarioCriarAtualizar(nome=nome, email=email, senha=senha)

    usuario = await usuario.criar_usuario(usuario_criar)

    if usuario:
        response = RedirectResponse(url='/login', status_code=303)
        return response

    return templates.TemplateResponse(request=request, name='registro.html', context={'error': 'Não foi possível criar o usuário, tente novamente mais tarde.', **data})