from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_inscricoes_body(request: Any, next_handler: Callable):
    body = request.get_json()
    if not body or "inscricoes" not in body or not isinstance(body["inscricoes"], dict):
        raise ErrorResponse(400, "Body invalido", {"message": "O JSON deve conter o objeto inscricoes"})

    insc = body["inscricoes"]
    if not insc.get("eventoId") or not str(insc.get("eventoId")).strip():
        raise ErrorResponse(400, "Campo obrigatorio", {"message": "O campo inscricoes.eventoId e obrigatorio"})

    return next_handler(request)
