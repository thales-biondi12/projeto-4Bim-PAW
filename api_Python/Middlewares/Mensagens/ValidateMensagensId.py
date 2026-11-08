from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_mensagens_id(request: Any, next_handler: Callable):
    id_mensagens = request.view_args.get("idMensagens") if request.view_args else request.args.get("idMensagens")
    if not id_mensagens or not str(id_mensagens).isdigit() or int(id_mensagens) <= 0:
        raise ErrorResponse(400, "Id invalido", {"message": "O parametro idMensagens deve ser um inteiro maior que zero"})

    return next_handler(request)
