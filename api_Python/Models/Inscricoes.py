from typing import Optional

class Inscricoes:
    def __init__(self):
        self.id_inscricoes = None
        self.usuario_id = None
        self.evento_id = None
        self.data_inscricao = ""
        self.presenca = ""
        self.nome_usuario = None
        self.titulo_evento = None

    def get_id_inscricoes(self) -> Optional[int]:
        return self.id_inscricoes

    def set_id_inscricoes(self, value: int):
        if value <= 0:
            raise ValueError("idInscricoes deve ser maior que zero.")
        self.id_inscricoes = value

    def get_usuario_id(self) -> Optional[int]:
        return self.usuario_id

    def set_usuario_id(self, value: int):
        if value <= 0:
            raise ValueError("usuarioId deve ser maior que zero.")
        self.usuario_id = value

    def get_evento_id(self) -> Optional[int]:
        return self.evento_id

    def set_evento_id(self, value: int):
        if value <= 0:
            raise ValueError("eventoId deve ser maior que zero.")
        self.evento_id = value

    def get_data_inscricao(self) -> Optional[str]:
        return self.data_inscricao

    def set_data_inscricao(self, value: str):
        data = value.isoformat() if hasattr(value, "isoformat") else str(value).strip()
        if not data:
            raise ValueError("dataInscricao nao pode ser vazia.")
        self.data_inscricao = data

    def get_presenca(self) -> Optional[str]:
        return self.presenca

    def set_presenca(self, value: str):
        presenca = value.strip()
        if not presenca:
            raise ValueError("presenca nao pode ser vazia.")
        self.presenca = presenca

    def get_nome_usuario(self) -> Optional[str]:
        return self.nome_usuario

    def set_nome_usuario(self, value: Optional[str]):
        self.nome_usuario = value

    def get_titulo_evento(self) -> Optional[str]:
        return self.titulo_evento

    def set_titulo_evento(self, value: Optional[str]):
        self.titulo_evento = value

    def to_dict(self) -> dict:
        return {
            "idInscricoes": self.get_id_inscricoes(),
            "usuarioId": self.get_usuario_id(),
            "eventoId": self.get_evento_id(),
            "dataInscricao": self.get_data_inscricao(),
            "presenca": self.get_presenca(),
            "nomeUsuario": self.get_nome_usuario(),
            "tituloEvento": self.get_titulo_evento(),
        }
