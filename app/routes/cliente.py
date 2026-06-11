from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db.cliente_repository import ClienteRepository
from app.models.cliente import Cliente, ClienteCriarAtualizar
from app.dependencies import get_cliente_repository

router = APIRouter(
    prefix='/api/clientes'
)

front_router = APIRouter(
    prefix='/clientes'
)

templates = Jinja2Templates(directory='templates')

@router.get('/', response_model=list[Cliente])
async def listar_clientes(cliente_repository: Annotated[ClienteRepository, Depends(get_cliente_repository)]):
    return await cliente_repository.listar_clientes()

@router.get('/{cliente_id}', response_model=Cliente | None)
async def obter_cliente(cliente_repository: Annotated[ClienteRepository, Depends(get_cliente_repository)], cliente_id: int):
    cliente = await cliente_repository.obter_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail='Cliente não encontrado!')
    return cliente

@router.post('/', response_model=Cliente, status_code=201)
async def criar_cliente(cliente_repository: Annotated[ClienteRepository, Depends(get_cliente_repository)], cliente: ClienteCriarAtualizar):
    return await cliente_repository.criar_cliente(cliente)

@router.put('/{cliente_id}', response_model=Cliente | None)
async def atualizar_cliente(cliente_repository: Annotated[ClienteRepository, Depends(get_cliente_repository)], cliente_id: int, cliente: ClienteCriarAtualizar):
    cliente_atualizado = await cliente_repository.atualizar_cliente(cliente_id, cliente)
    if not cliente_atualizado:
        raise HTTPException(status_code=404, detail='Cliente não encontrado!')
    return cliente_atualizado

@router.delete('/{cliente_id}', status_code=204)
async def deletar_cliente(cliente_repository: Annotated[ClienteRepository, Depends(get_cliente_repository)], cliente_id: int):
    sucesso = await cliente_repository.deletar_cliente(cliente_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail='Cliente não encontrado!')

@front_router.get('/', response_class=HTMLResponse)
async def pagina_listar_clientes(request: Request, cliente_repository: Annotated[ClienteRepository, Depends(get_cliente_repository)]):
    clientes = await cliente_repository.listar_clientes()
    return templates.TemplateResponse(request=request, name='clientes.html', context={'clientes': clientes, 'titulo': 'Lista de Clientes'})

@front_router.get('/novo', response_class=HTMLResponse)
async def pagina_criar_cliente(request: Request):
    return templates.TemplateResponse(request=request, name='cliente-form.html')

@front_router.get('/{cliente_id}', response_class=HTMLResponse)
async def pagina_editar_cliente(request: Request, cliente_id: int, cliente_repository: Annotated[ClienteRepository, Depends(get_cliente_repository)]):
    cliente = await cliente_repository.obter_cliente(cliente_id)
    return templates.TemplateResponse(request=request, name='clientes-form.html', context={'cliente': cliente})