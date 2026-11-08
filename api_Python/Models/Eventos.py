from typing import Optional
class Eventos:
    def __init__(self):
        self.id_evento = None
        self.titulo = ""
        self.descricao = ""
        self.data_evento = ""
        self.local_evento = ""
        self.limite_vagas = None
        self.status_evento = ""

    def get_id_evento(self) -> Optional[int]:
        return self.id_evento

    def set_id_evento(self, value: int):
        if value <= 0:
            raise ValueError("idEvento deve ser maior que zero.")
        self.id_evento = value

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

    def get_descricao(self) -> Optional[str]:
        return self.descricao

    def set_descricao(self, value: str):
        descricao = value.strip()
        if not descricao:
            raise ValueError("descricao nao pode ser vazia.")
        self.descricao = descricao

    def get_data_evento(self) -> Optional[str]:
        return self.data_evento

    def set_data_evento(self, value: str):
        data = value.isoformat() if hasattr(value, "isoformat") else str(value).strip()
        if not data:
            raise ValueError("dataEvento nao pode ser vazia.")
        self.data_evento = data

    def get_local_evento(self) -> Optional[str]:
        return self.local_evento

    def set_local_evento(self, value: str):
        local = value.strip()
        if not local:
            raise ValueError("localEvento nao pode ser vazio.")
        self.local_evento = local

    def get_limite_vagas(self) -> Optional[int]:
        return self.limite_vagas

    def set_limite_vagas(self, value: int):
        if value < 0:
            raise ValueError("limiteVagas nao pode ser negativo.")
        self.limite_vagas = value

    def get_status_evento(self) -> Optional[str]:
        return self.status_evento

    def set_status_evento(self, value: str):
        status = value.strip()
        if not status:
            raise ValueError("statusEvento nao pode ser vazio.")
        self.status_evento = status

    def to_dict(self) -> dict:
        return {
            "idEvento": self.get_id_evento(),
            "titulo": self.get_titulo(),
            "descricao": self.get_descricao(),
            "dataEvento": self.get_data_evento(),
            "localEvento": self.get_local_evento(),
            "limiteVagas": self.get_limite_vagas(),
            "statusEvento": self.get_status_evento(),
        }
