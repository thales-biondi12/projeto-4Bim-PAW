from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_inscricoes_id(request: Any, next_handler: Callable):
    id_inscricoes = request.view_args.get("idInscricoes") if request.view_args else request.args.get("idInscricoes")
    if not id_inscricoes or not str(id_inscricoes).isdigit() or int(id_inscricoes) <= 0:
        raise ErrorResponse(400, "Id invalido", {"message": "O parametro idInscricoes deve ser um inteiro maior que zero"})

    return next_handler(request)
