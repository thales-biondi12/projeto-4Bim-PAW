from typing import Any, Callable
from ...Http.ErrorResponse import ErrorResponse
from ...Http.MeuTokenJWT import MeuTokenJWT

def validate_inscricoes_token(request: Any, next_handler: Callable):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise ErrorResponse(401, "Acesso não autorizado", {"message": "Token de autenticação não informado"})

    if not auth_header.startswith("Bearer "):
        raise ErrorResponse(401, "Acesso não autorizado", {"message": "Formato do token inválido"})

    jwt = MeuTokenJWT()
    if not jwt.validate_token(auth_header):
        raise ErrorResponse(401, "Acesso não autorizado", {"message": "Token inválido ou expirado"})

    request.jwt_payload = jwt.get_payload()
    return next_handler(request)
