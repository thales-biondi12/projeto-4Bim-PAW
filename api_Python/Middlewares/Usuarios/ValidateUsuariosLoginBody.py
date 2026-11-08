import re
from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_usuarios_login_body(request: Any, next_handler: Callable):
    body = request.get_json()
    if not body:
        raise ErrorResponse(400, "Erro na validação de dados", {"message": "Body JSON inválido ou vazio"})

    dados = body.get("usuarios") or body.get("usuario") or body.get("funcionario")
    if not isinstance(dados, dict):
        raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'usuarios' é obrigatório!"})

    email = str(dados.get("email", "")).strip()
    if not email:
        raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'email' é obrigatório!"})

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ErrorResponse(400, "Erro na validação de dados", {"message": "Email inválido!"})

    if not str(dados.get("senha", "")).strip():
        raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'senha' é obrigatório!"})

    return next_handler(request)
