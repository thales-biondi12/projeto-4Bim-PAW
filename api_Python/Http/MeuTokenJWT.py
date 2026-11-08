import jwt
import datetime
import secrets
from typing import Optional, Any

class MeuTokenJWT:
    """
    Classe responsável pela geração e validação de tokens JWT.
    """
    KEY = "x9S4q0v+V0IjvHkG20uAxaHx1ijj+q1HWjHKv+ohxp/oK+77qyXkVj/l4QYHHTF3"
    ALGORITHM = "HS256"
    TYPE = "JWT"

    def __init__(self):
        self.payload = None
        self.iss = "http://localhost"
        self.aud = "http://localhost"
        self.sub = "acesso_sistema"
        # 30 dias
        self.duration = 3600 * 24 * 30

    def gerar_token(self, claims: Any) -> str:
        """
        Gera um token JWT.
        """
        # Normaliza claims para suportar múltiplos padrões (Usuarios/Funcionario/etc)
        # Suporta tanto objeto quanto dicionário
        def get_val(obj, keys):
            if isinstance(obj, dict):
                for k in keys:
                    if k in obj: return obj[k]
            else:
                for k in keys:
                    if hasattr(obj, k): return getattr(obj, k)
            return None

        id_usuario = get_val(claims, ["idUsuario", "idFuncionario", "id"])
        nome = get_val(claims, ["nomeUsuario", "name", "nome"])
        email = get_val(claims, ["email"])
        tipo = get_val(claims, ["tipoUsuario", "role", "tipo_usuario"])

        dados_usuario = {
            "idUsuario": id_usuario,
            "nomeUsuario": nome,
            "email": email,
            "tipoUsuario": tipo,
        }

        dados_funcionario = {
            "idFuncionario": id_usuario,
            "idUsuario": id_usuario,
            "name": nome,
            "nomeUsuario": nome,
            "email": email,
            "role": tipo,
            "tipoUsuario": tipo,
        }

        now = datetime.datetime.utcnow()
        payload = {
            "iss": self.iss,
            "aud": self.aud,
            "sub": self.sub,
            "iat": now,
            "nbf": now,
            "exp": now + datetime.timedelta(seconds=self.duration),
            "jti": secrets.token_hex(16),
            "usuario": dados_usuario,
            "funcionario": dados_funcionario,
        }

        return jwt.encode(payload, self.KEY, algorithm=self.ALGORITHM)

    def validate_token(self, string_token: str) -> bool:
        if not string_token:
            return False

        token = string_token.strip()
        if token.startswith("Bearer "):
            token = token[7:]

        try:
            payload = jwt.decode(token, self.KEY, algorithms=[self.ALGORITHM], audience=self.aud, issuer=self.iss)

            if payload.get("sub") != self.sub:
                return False

            self.payload = payload
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception):
            return False

    def get_payload(self) -> Optional[dict]:
        return self.payload

    def set_payload(self, payload: Optional[dict]):
        self.payload = payload
        return self

    def limpar_payload(self):
        self.payload = None
        return self

    def get_iss(self) -> str: return self.iss
    def set_iss(self, iss: str): self.iss = iss; return self
    def get_aud(self) -> str: return self.aud
    def set_aud(self, aud: str): self.aud = aud; return self
    def get_sub(self) -> str: return self.sub
    def set_sub(self, sub: str): self.sub = sub; return self
    def get_duration(self) -> int: return self.duration
    def set_duration(self, duration: int): self.duration = duration; return self
