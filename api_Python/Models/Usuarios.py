import re
from typing import Optional

class Usuarios:
    def __init__(self):
        self.id_usuario = 0
        self.nome_usuario = ""
        self.email = ""
        self.senha = ""
        self.tel = ""
        self.tipo_usuario = ""
        self.data_nasc = ""

    def get_id_usuario(self) -> Optional[int]:
        return self.id_usuario

    def set_id_usuario(self, value: int):
        if value <= 0:
            raise ValueError("idUsuario deve ser maior que zero.")
        self.id_usuario = value

    def get_id_usuarios(self) -> Optional[int]:
        return self.get_id_usuario()

    def set_id_usuarios(self, value: int):
        self.set_id_usuario(value)

    def get_nome_usuario(self) -> Optional[str]:
        return self.nome_usuario

    def set_nome_usuario(self, value: str):
        nome = value.strip()
        if not nome:
            raise ValueError("nomeUsuario nao pode ser vazio.")
        if len(nome) < 3:
            raise ValueError("nomeUsuario deve ter pelo menos 3 caracteres.")
        if len(nome) > 100:
            raise ValueError("nomeUsuario muito grande.")
        self.nome_usuario = nome

    def get_nome(self) -> Optional[str]:
        return self.get_nome_usuario()

    def set_email(self, email: str):
        email = email.strip()
        if not email:
            raise ValueError("email nao pode ser vazio.")
        # Regex simples para validação de email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("email invalido.")
        self.email = email

    def get_email(self) -> Optional[str]:
        return self.email

    def set_senha(self, senha: str):
        if not senha.strip():
            raise ValueError("senha nao pode ser vazia.")
        self.senha = senha

    def get_senha(self) -> Optional[str]:
        return self.senha

    def set_tel(self, tel: Optional[str]):
        self.tel = tel.strip() if tel else ""

    def get_tel(self) -> Optional[str]:
        return self.tel

    def set_tipo_usuario(self, tipo_usuario: Optional[str]):
        self.tipo_usuario = tipo_usuario.strip() if tipo_usuario else ""

    def get_tipo_usuario(self) -> Optional[str]:
        return self.tipo_usuario

    def set_data_nasc(self, data_nasc: Optional[str]):
        self.data_nasc = data_nasc.isoformat() if hasattr(data_nasc, "isoformat") else (str(data_nasc).strip() if data_nasc else "")

    def get_data_nasc(self) -> Optional[str]:
        return self.data_nasc

    def to_dict(self) -> dict:
        return {
            "idUsuario": self.get_id_usuario(),
            "nomeUsuario": self.get_nome_usuario(),
            "email": self.get_email(),
            "tel": self.get_tel(),
            "tipoUsuario": self.get_tipo_usuario(),
            "data_nasc": self.get_data_nasc(),
        }
