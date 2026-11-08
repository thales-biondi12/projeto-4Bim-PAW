import logging
from datetime import datetime
from typing import List, Optional, Any
from ..Models.Inscricoes import Inscricoes
from ..Dao.InscricaoDao import InscricaoDao
from ..Dao.UsuariosDao import UsuariosDao
from ..Dao.EventosDao import EventosDao
from ..Http.ErrorResponse import ErrorResponse

class InscricoesService:
    def __init__(self, inscricao_dao_dep: InscricaoDao, usuarios_dao_dep: UsuariosDao, eventos_dao_dep: EventosDao):
        self.inscricao_dao = inscricao_dao_dep
        self.usuarios_dao = usuarios_dao_dep
        self.eventos_dao = eventos_dao_dep
        logging.info("⬆️ InscricoesService::__init__")

    def create_service(self, data: Any) -> Inscricoes:
        logging.info("🟣 InscricoesService::create_service")

        insc_data = data.get("inscricoes", {}) if isinstance(data, dict) else getattr(data, "inscricoes", {})

        usuario_id = (insc_data.get("usuarioId") if isinstance(insc_data, dict) else getattr(insc_data, "usuarioId", None))
        evento_id = (insc_data.get("eventoId") if isinstance(insc_data, dict) else getattr(insc_data, "eventoId", None))
        data_inscricao = (insc_data.get("dataInscricao") if isinstance(insc_data, dict) else getattr(insc_data, "dataInscricao", None))
        presenca = (insc_data.get("presenca") if isinstance(insc_data, dict) else getattr(insc_data, "presenca", None))

        if not usuario_id or not self.usuarios_dao.find_by_id(usuario_id):
            raise ErrorResponse(400, "Usuário não encontrado", {"message": f"O usuário com id {usuario_id} não existe."})

        if not evento_id or not self.eventos_dao.find_by_id(evento_id):
            raise ErrorResponse(400, "Evento não encontrado", {"message": f"O evento com id {evento_id} não existe."})

        inscricoes_usuario = self.inscricao_dao.find_by_field("usuario_id", usuario_id)
        for insc in inscricoes_usuario:
            if insc.get_evento_id() == evento_id:
                raise ErrorResponse(400, "Inscrição duplicada", {"message": "Usuário já inscrito neste evento."})

        eventos_inscricoes = self.inscricao_dao.find_by_field("evento_id", evento_id)
        evento = self.eventos_dao.find_by_id(evento_id)
        if evento and evento.get_limite_vagas() > 0 and len(eventos_inscricoes) >= evento.get_limite_vagas():
            raise ErrorResponse(400, "Evento sem vagas", {"message": "Não há vagas disponíveis neste evento."})

        if not data_inscricao:
            data_inscricao = datetime.now().strftime("%Y-%m-%d")

        inscricao = Inscricoes()
        inscricao.set_usuario_id(usuario_id)
        inscricao.set_evento_id(evento_id)
        inscricao.set_data_inscricao(data_inscricao)
        inscricao.set_presenca(presenca)

        return self.inscricao_dao.create(inscricao)

    def count_service(self) -> int:
        logging.info("🟣 InscricoesService::count_service")
        return self.inscricao_dao.count()

    def find_all_service(self) -> List[Inscricoes]:
        logging.info("🟣 InscricoesService::find_all_service")
        return self.inscricao_dao.find_all()

    def find_by_id_service(self, id_inscricoes: int) -> Optional[Inscricoes]:
        logging.info("🟣 InscricoesService::find_by_id_service")
        return self.inscricao_dao.find_by_id(id_inscricoes)

    def update_service(self, id_inscricoes: int, data: Any) -> Inscricoes:
        logging.info("🟣 InscricoesService::update_service")

        inscricao_existente = self.inscricao_dao.find_by_id(id_inscricoes)
        if not inscricao_existente:
            raise ErrorResponse(404, "Inscricao não encontrada", {"message": f"Não existe inscrição com id {id_inscricoes}"})

        insc_data = data.get("inscricoes", {}) if isinstance(data, dict) else getattr(data, "inscricoes", {})

        usuario_id = (insc_data.get("usuarioId") if isinstance(insc_data, dict) else getattr(insc_data, "usuarioId", None))
        evento_id = (insc_data.get("eventoId") if isinstance(insc_data, dict) else getattr(insc_data, "eventoId", None))
        data_inscricao = (insc_data.get("dataInscricao") if isinstance(insc_data, dict) else getattr(insc_data, "dataInscricao", None))
        presenca = (insc_data.get("presenca") if isinstance(insc_data, dict) else getattr(insc_data, "presenca", None))

        if not usuario_id or not self.usuarios_dao.find_by_id(usuario_id):
            raise ErrorResponse(400, "Usuário não encontrado", {"message": f"O usuário com id {usuario_id} não existe."})

        if not evento_id or not self.eventos_dao.find_by_id(evento_id):
            raise ErrorResponse(400, "Evento não encontrado", {"message": f"O evento com id {evento_id} não existe."})

        inscricoes_usuario = self.inscricao_dao.find_by_field("usuario_id", usuario_id)
        for insc in inscricoes_usuario:
            if insc.get_evento_id() == evento_id and insc.get_id_inscricoes() != id_inscricoes:
                raise ErrorResponse(400, "Inscrição duplicada", {"message": "Usuário já inscrito neste evento."})

        evento = self.eventos_dao.find_by_id(evento_id)
        eventos_inscricoes = self.inscricao_dao.find_by_field("evento_id", evento_id)
        if evento and evento.get_limite_vagas() > 0 and \
           inscricao_existente.get_evento_id() != evento_id and \
           len(eventos_inscricoes) >= evento.get_limite_vagas():
            raise ErrorResponse(400, "Evento sem vagas", {"message": "Não há vagas disponíveis neste evento."})

        if not data_inscricao:
            data_inscricao = datetime.now().strftime("%Y-%m-%d")

        inscricao_existente.set_usuario_id(usuario_id)
        inscricao_existente.set_evento_id(evento_id)
        inscricao_existente.set_data_inscricao(data_inscricao)
        inscricao_existente.set_presenca(presenca)

        self.inscricao_dao.update(inscricao_existente)
        return inscricao_existente

    def delete_service(self, id_inscricoes: int) -> bool:
        logging.info("🟣 InscricoesService::delete_service")
        inscricao_existente = self.inscricao_dao.find_by_id(id_inscricoes)
        if not inscricao_existente:
            raise ErrorResponse(404, "Inscricao não encontrada", {"message": f"Não existe inscrição com id {id_inscricoes}"})

        return self.inscricao_dao.delete(inscricao_existente)
