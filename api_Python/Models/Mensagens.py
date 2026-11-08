from typing import Optional

class Mensagens:
    def __init__(self):
        self.id_mensagens = None
        self.titulo = ""
        self.conteudo = ""
        self.usuario_id = None
        self.data_postagem = ""

    def get_id_mensagens(self) -> Optional[int]:
        return self.id_mensagens

    def set_id_mensagens(self, value: int):
        if value <= 0:
            raise ValueError("idMensagens deve ser maior que zero.")
        self.id_mensagens = value

    def get_titulo(self) -> Optional[str]:
        return self.titulo

    def set_titulo(self, value: str):
        titulo = value.strip()
        if not titulo:
            raise ValueError("titulo nao pode ser vazio.")
        if len(titulo) < 3:
            raise ValueError("titulo deve ter pelo menos 3 caracteres.")
        if len(titulo) > 100:
            raise ValueError("titulo muito grande.")
        self.titulo = titulo

    def get_conteudo(self) -> Optional[str]:
        return self.conteudo

    def set_conteudo(self, value: str):
        conteudo = value.strip()
        if not conteudo:
            raise ValueError("conteudo nao pode ser vazio.")
        self.conteudo = conteudo

    def get_usuario_id(self) -> Optional[int]:
        return self.usuario_id

    def set_usuario_id(self, value: int):
        if value <= 0:
            raise ValueError("usuarioId deve ser maior que zero.")
        self.usuario_id = value

    def get_data_postagem(self) -> Optional[str]:
        return self.data_postagem

    def set_data_postagem(self, value: str):
        data = value.isoformat() if hasattr(value, "isoformat") else str(value).strip()
        if not data:
            raise ValueError("dataPostagem nao pode ser vazia.")
        self.data_postagem = data

    def to_dict(self) -> dict:
        return {
            "idMensagens": self.get_id_mensagens(),
            "titulo": self.get_titulo(),
            "conteudo": self.get_conteudo(),
            "usuarioId": self.get_usuario_id(),
            "dataPostagem": self.get_data_postagem(),
        }
