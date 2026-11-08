from typing import Optional

class Ministerios:
    def __init__(self):
        self.id_ministerios = None
        self.nome = ""
        self.descricao = ""
        self.dia_reuniao = ""
        self.id_coordenador = None
        self.nome_coordenador = None

    def get_id_ministerios(self) -> Optional[int]:
        return self.id_ministerios

    def set_id_ministerios(self, value: int):
        if value <= 0:
            raise ValueError("idMinisterios deve ser maior que zero.")
        self.id_ministerios = value

    def get_nome(self) -> Optional[str]:
        return self.nome

    def set_nome(self, value: str):
        nome = value.strip()
        if not nome:
            raise ValueError("nome nao pode ser vazio.")
        if len(nome) < 3:
            raise ValueError("nome deve ter pelo menos 3 caracteres.")
        if len(nome) > 100:
            raise ValueError("nome muito grande.")
        self.nome = nome

    def get_descricao(self) -> Optional[str]:
        return self.descricao

    def set_descricao(self, value: str):
        self.descricao = value.strip()

    def get_dia_reuniao(self) -> Optional[str]:
        return self.dia_reuniao

    def set_dia_reuniao(self, value: str):
        dia = value.strip()
        if not dia:
            raise ValueError("diaReuniao nao pode ser vazio.")
        self.dia_reuniao = dia

    def get_id_coordenador(self) -> Optional[int]:
        return self.id_coordenador

    def set_id_coordenador(self, value: int):
        if value <= 0:
            raise ValueError("idCoordenador deve ser maior que zero.")
        self.id_coordenador = value

    def get_nome_coordenador(self) -> Optional[str]:
        return self.nome_coordenador

    def set_nome_coordenador(self, value: Optional[str]):
        self.nome_coordenador = value

    def to_dict(self) -> dict:
        return {
            "idMinisterios": self.get_id_ministerios(),
            "nome": self.get_nome(),
            "descricao": self.get_descricao(),
            "diaReuniao": self.get_dia_reuniao(),
            "idCoordenador": self.get_id_coordenador(),
            "nomeCoordenador": self.get_nome_coordenador(),
        }
