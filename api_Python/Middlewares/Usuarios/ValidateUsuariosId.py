from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_usuarios_id(request: Any, next_handler: Callable):
    id_usuario = request.view_args.get("idUsuario") if request.view_args else request.args.get("idUsuario")
    if not id_usuario or not str(id_usuario).isdigit() or int(id_usuario) <= 0:
        raise ErrorResponse(400, "Id invalido", {"message": "O parametro idUsuario deve ser um inteiro maior que zero"})

    return next_handler(request)
