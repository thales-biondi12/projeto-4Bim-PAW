from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_usuarios_body(request: Any, next_handler: Callable, require_password: bool = True):
    body = request.get_json()
    if not body or "usuarios" not in body or not isinstance(body["usuarios"], dict):
        raise ErrorResponse(400, "Body invalido", {"message": "O JSON deve conter o objeto usuarios"})

    usuarios = body["usuarios"]
    # A API aceita tanto o nome usado pelo modelo/frontend (nome)
    # quanto o formato legado (nomeUsuario).
    if not str(usuarios.get("nomeUsuario") or usuarios.get("nome") or "").strip():
        raise ErrorResponse(400, "Campo obrigatorio", {"message": "O campo usuarios.nome ou usuarios.nomeUsuario e obrigatorio"})

    required_fields = ["email"]
    if require_password:
        required_fields.append("senha")
    for field in required_fields:
        if not str(usuarios.get(field, "")).strip():
            raise ErrorResponse(400, "Campo obrigatorio", {"message": f"O campo usuarios.{field} e obrigatorio"})

    return next_handler(request)
