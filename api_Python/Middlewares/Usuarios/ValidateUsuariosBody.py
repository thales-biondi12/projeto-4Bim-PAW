from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_usuarios_body(request: Any, next_handler: Callable):
    body = request.get_json()
    if not body or "usuarios" not in body or not isinstance(body["usuarios"], dict):
        raise ErrorResponse(400, "Body invalido", {"message": "O JSON deve conter o objeto usuarios"})

    usuarios = body["usuarios"]
    for field in ["nomeUsuario", "email", "senha"]:
        if not str(usuarios.get(field, "")).strip():
            raise ErrorResponse(400, "Campo obrigatorio", {"message": f"O campo usuarios.{field} e obrigatorio"})

    return next_handler(request)
