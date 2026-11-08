from typing import Optional

class UsuarioMinisterio:
    def __init__(self):
        self.id = None
        self.id_usuario = None
        self.id_ministerio = None
        self.data_entrada = ""
        self.funcao = ""
        self.nome_usuario = None
        self.nome_ministerio = None

    def get_id(self) -> Optional[int]:
        return self.id

    def set_id(self, value: int):
        self.id = value

    def get_id_usuario(self) -> Optional[int]:
        return self.id_usuario

    def set_id_usuario(self, value: int):
        self.id_usuario = value

    def get_id_ministerio(self) -> Optional[int]:
        return self.id_ministerio

    def set_id_ministerio(self, value: int):
        self.id_ministerio = value

    def get_data_entrada(self) -> str:
        return self.data_entrada

    def set_data_entrada(self, value: str):
        self.data_entrada = value.isoformat() if hasattr(value, "isoformat") else value

    def get_funcao(self) -> str:
        return self.funcao

    def set_funcao(self, value: str):
        self.funcao = value

    def get_nome_usuario(self) -> Optional[str]:
        return self.nome_usuario

    def set_nome_usuario(self, value: Optional[str]):
        self.nome_usuario = value

    def get_nome_ministerio(self) -> Optional[str]:
        return self.nome_ministerio

    def set_nome_ministerio(self, value: Optional[str]):
        self.nome_ministerio = value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "idUsuario": self.id_usuario,
            "idMinisterio": self.id_ministerio,
            "dataEntrada": self.data_entrada,
            "funcao": self.funcao,
            "nomeUsuario": self.nome_usuario,
            "nomeMinisterio": self.nome_ministerio,
        }
