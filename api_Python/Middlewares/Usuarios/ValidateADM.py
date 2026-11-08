from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse

def validate_adm(request: Any, next_handler: Callable):
    payload = getattr(request, "jwt_payload", None)
    if not payload:
        raise ErrorResponse(401, "Acesso não autorizado", {"message": "Usuário não autenticado"})

    # Suporta múltiplos formatos de payload
    tipo = None
    usuario = payload.get("usuario", {})
    funcionario = payload.get("funcionario", {})

    tipo = usuario.get("tipoUsuario") or funcionario.get("role") or funcionario.get("tipoUsuario")

    if not tipo:
        raise ErrorResponse(403, "Acesso negado", {"message": "Tipo de usuário não identificado"})

    tipo_norm = str(tipo).strip().upper()
    if tipo_norm not in ["ADM", "ADMINISTRADOR", "ADMINISTRATOR"]:
        raise ErrorResponse(403, "Acesso negado", {"message": "Apenas administradores possuem acesso"})

    return next_handler(request)
