from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_ministerios_id(request: Any, next_handler: Callable):
    id_ministerio = request.view_args.get("idMinisterios") if request.view_args else request.args.get("idMinisterios")
    if not id_ministerio or not str(id_ministerio).isdigit() or int(id_ministerio) <= 0:
        raise ErrorResponse(400, "Id invalido", {"message": "O parametro idMinisterio deve ser um inteiro maior que zero"})

    return next_handler(request)
