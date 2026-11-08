from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_mensagens_body(request: Any, next_handler: Callable):
    body = request.get_json()
    if not body or "mensagens" not in body or not isinstance(body["mensagens"], dict):
        raise ErrorResponse(400, "Body invalido", {"message": "O JSON deve conter o objeto mensagens"})

    msg = body["mensagens"]
    for field in ["titulo", "conteudo"]:
        if not str(msg.get(field, "")).strip():
            raise ErrorResponse(400, "Campo obrigatorio", {"message": f"O campo mensagens.{field} e obrigatorio"})

    return next_handler(request)
