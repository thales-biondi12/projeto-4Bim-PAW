from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_eventos_body(request: Any, next_handler: Callable):
    body = request.get_json()
    if not body or "eventos" not in body or not isinstance(body["eventos"], dict):
        raise ErrorResponse(400, "Body invalido", {"message": "O JSON deve conter o objeto eventos"})

    eventos = body["eventos"]
    map_fields = {
        "titulo": "titulo",
        "descricao": "descricao",
        "dataEvento": "data_evento",
        "localEvento": "local_evento",
        "limiteVagas": "limite_vagas",
        "statusEvento": "status_evento",
    }
    for camel, snake in map_fields.items():
        val = eventos.get(camel) or eventos.get(snake, "")
        if not str(val).strip():
            raise ErrorResponse(400, "Campo obrigatorio", {"message": f"O campo eventos.{camel} e obrigatorio"})

    return next_handler(request)
