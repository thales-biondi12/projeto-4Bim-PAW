import logging
from typing import List, Optional, Any
from ..Models.Ministerios import Ministerios
from ..Dao.MinisterioDao import MinisterioDao
from ..Dao.UsuariosDao import UsuariosDao
from ..Http.ErrorResponse import ErrorResponse

class MinisteriosService:
    def __init__(self, ministerio_dao_dep: MinisterioDao, usuarios_dao_dep: UsuariosDao):
        self.ministerio_dao = ministerio_dao_dep
        self.usuarios_dao = usuarios_dao_dep
        logging.info("⬆️ MinisteriosService::__init__")

    def _validate_coordinator(self, id_coordenador: int):
        if not self.usuarios_dao.find_by_id(id_coordenador):
            raise ErrorResponse(400, "Coordenador não encontrado", {
                "message": f"O usuário com id {id_coordenador} não existe. Verifique o id do coordenador."
            })

    def create_service(self, data: Any) -> Ministerios:
        logging.info("🟣 MinisteriosService::create_service")

        min_data = data.get("ministerios", {}) if isinstance(data, dict) else getattr(data, "ministerios", {})

        id_coord = (min_data.get("idCoordenador") or min_data.get("id_coordenador", 0)) if isinstance(min_data, dict) else \
                   (getattr(min_data, "idCoordenador", getattr(min_data, "id_coordenador", 0)))

        dia = (min_data.get("diaReuniao") or min_data.get("dia_reuniao")) if isinstance(min_data, dict) else \
              (getattr(min_data, "diaReuniao", getattr(min_data, "dia_reuniao", None)))

        self._validate_coordinator(int(id_coord))

        ministerio = Ministerios()
        nome = (min_data.get("nome") if isinstance(min_data, dict) else getattr(min_data, "nome", ""))
        ministerio.set_nome(nome)
        ministerio.set_descricao(min_data.get("descricao") if isinstance(min_data, dict) else getattr(min_data, "descricao", None))
        ministerio.set_dia_reuniao(dia)
        ministerio.set_id_coordenador(int(id_coord))

        resultado = self.ministerio_dao.find_by_field("nome", ministerio.get_nome())
        if len(resultado) > 0:
            raise ErrorResponse(400, "Ministério já existe", {"message": f"O ministério {ministerio.get_nome()} já está cadastrado"})

        return self.ministerio_dao.create(ministerio)

    def count_service(self) -> int:
        logging.info("🟣 MinisteriosService::count_service")
        return self.ministerio_dao.count()

    def find_all_service(self) -> List[Ministerios]:
        logging.info("🟣 MinisteriosService::find_all_service")
        return self.ministerio_dao.find_all()

    def find_by_id_service(self, id_ministerio: int) -> Optional[Ministerios]:
        logging.info("🟣 MinisteriosService::find_by_id_service")
        return self.ministerio_dao.find_by_id(id_ministerio)

    def update_service(self, id_ministerio: int, data: Any) -> Ministerios:
        logging.info("🟣 MinisteriosService::update_service")

        min_data = data.get("ministerios", {}) if isinstance(data, dict) else getattr(data, "ministerios", {})

        id_coord = (min_data.get("idCoordenador") or min_data.get("id_coordenador", 0)) if isinstance(min_data, dict) else \
                   (getattr(min_data, "idCoordenador", getattr(min_data, "id_coordenador", 0)))

        dia = (min_data.get("diaReuniao") or min_data.get("dia_reuniao")) if isinstance(min_data, dict) else \
              (getattr(min_data, "diaReuniao", getattr(min_data, "dia_reuniao", None)))

        self._validate_coordinator(int(id_coord))

        ministerio_existente = self.ministerio_dao.find_by_id(id_ministerio)
        if not ministerio_existente:
            raise ErrorResponse(404, "Ministério não encontrado", {"message": f"Não existe ministério com id {id_ministerio}"})

        ministerio_existente.set_nome(min_data.get("nome") if isinstance(min_data, dict) else getattr(min_data, "nome", ""))
        ministerio_existente.set_descricao(min_data.get("descricao") if isinstance(min_data, dict) else getattr(min_data, "descricao", None))
        ministerio_existente.set_dia_reuniao(dia)
        ministerio_existente.set_id_coordenador(int(id_coord))

        self.ministerio_dao.update(ministerio_existente)
        return ministerio_existente

    def delete_service(self, id_ministerio: int) -> bool:
        logging.info("🟣 MinisteriosService::delete_service")
        ministerio_existente = self.ministerio_dao.find_by_id(id_ministerio)
        if not ministerio_existente:
            raise ErrorResponse(404, "Ministério não encontrado", {"message": f"Não existe ministério com id {id_ministerio}"})

        return self.ministerio_dao.delete(ministerio_existente)
