from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_ministerios_body(request: Any, next_handler: Callable):
    body = request.get_json()
    if not body or "ministerios" not in body or not isinstance(body["ministerios"], dict):
        raise ErrorResponse(400, "Body invalido", {"message": "O JSON deve conter o objeto ministerios"})

    ministerios = body["ministerios"]
    if not str(ministerios.get("nome", "")).strip():
        raise ErrorResponse(400, "Nome obrigatorio", {"message": "O campo ministerios.nome e obrigatorio"})

    return next_handler(request)
