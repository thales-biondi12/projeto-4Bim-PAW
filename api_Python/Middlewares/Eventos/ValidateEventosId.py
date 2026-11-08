from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_eventos_id(request: Any, next_handler: Callable):
    id_evento = request.view_args.get("idEvento") if request.view_args else request.args.get("idEvento")
    if not id_evento or not str(id_evento).isdigit() or int(id_evento) <= 0:
        raise ErrorResponse(400, "Id invalido", {"message": "O parametro idEvento deve ser um inteiro maior que zero"})

    return next_handler(request)
