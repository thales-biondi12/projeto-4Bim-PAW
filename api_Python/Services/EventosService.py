import logging
from datetime import datetime
from typing import List, Optional, Any
from ..Models.Eventos import Eventos
from ..Dao.EventosDao import EventosDao
from ..Http.ErrorResponse import ErrorResponse

class EventosService:
    """
    Camada de regra de negócio da entidade Eventos.
    """
    def __init__(self, eventos_dao_dependency: EventosDao):
        self.eventos_dao = eventos_dao_dependency
        logging.info("⬆️ EventosService::__init__")

    def create_service(self, data: Any) -> Eventos:
        logging.info("🟣 EventosService::create_service")

        # Suporta acesso via objeto ou dicionário (compatível com JSON)
        eventos_data = data.get("eventos", {}) if isinstance(data, dict) else getattr(data, "eventos", {})

        titulo = (eventos_data.get("titulo", "") if isinstance(eventos_data, dict) else getattr(eventos_data, "titulo", "")).strip()
        descricao = eventos_data.get("descricao") if isinstance(eventos_data, dict) else getattr(eventos_data, "descricao", None)

        data_evento_str = (eventos_data.get("dataEvento") or eventos_data.get("data_evento")) if isinstance(eventos_data, dict) else \
                         (getattr(eventos_data, "dataEvento", None) or getattr(eventos_data, "data_evento", None))

        local_evento = (eventos_data.get("localEvento") or eventos_data.get("local_evento")) if isinstance(eventos_data, dict) else \
                      (getattr(eventos_data, "localEvento", None) or getattr(eventos_data, "local_evento", None))

        limite_vagas = int((eventos_data.get("limiteVagas") or eventos_data.get("limite_vagas", 0)) if isinstance(eventos_data, dict) else \
                         (getattr(eventos_data, "limiteVagas", getattr(eventos_data, "limite_vagas", 0))))

        status_evento = (eventos_data.get("statusEvento") or eventos_data.get("status_evento")) if isinstance(eventos_data, dict) else \
                        (getattr(eventos_data, "statusEvento", getattr(eventos_data, "status_evento", None)))

        if not titulo:
            raise ErrorResponse(400, "Título inválido", {"message": "O título do evento não pode ser vazio."})

        existente = self.eventos_dao.find_by_field("titulo", titulo)
        if len(existente) > 0:
            raise ErrorResponse(400, "Evento já existe", {"message": f"O evento {titulo} já está cadastrado"})

        if not data_evento_str:
            raise ErrorResponse(400, "Data inválida", {"message": "A data do evento é obrigatória."})

        try:
            data_evento_dt = datetime.strptime(data_evento_str, "%Y-%m-%d")
        except ValueError:
            raise ErrorResponse(400, "Data inválida", {"message": "Formato de data inválido. Use YYYY-MM-DD."})

        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if data_evento_dt < hoje:
            raise ErrorResponse(400, "Data inválida", {"message": "A data do evento não pode ser anterior à data atual."})

        if limite_vagas < 0:
            raise ErrorResponse(400, "Limite inválido", {"message": "O limite de vagas deve ser maior ou igual a zero."})

        evento = Eventos()
        evento.set_titulo(titulo)
        evento.set_descricao(descricao)
        evento.set_data_evento(data_evento_dt.strftime("%Y-%m-%d"))
        evento.set_local_evento(local_evento)
        evento.set_limite_vagas(limite_vagas)
        evento.set_status_evento(status_evento)

        return self.eventos_dao.create(evento)

    def count_service(self) -> int:
        logging.info("🟣 EventosService::count_service")
        return self.eventos_dao.count()

    def find_all_service(self) -> List[Eventos]:
        logging.info("🟣 EventosService::find_all_service")
        return self.eventos_dao.find_all()

    def find_by_id_service(self, id_evento: int) -> Optional[Eventos]:
        logging.info("🟣 EventosService::find_by_id_service")
        return self.eventos_dao.find_by_id(id_evento)

    def update_service(self, id_evento: int, data: Any) -> Eventos:
        logging.info("🟣 EventosService::update_service")

        evento_existente = self.eventos_dao.find_by_id(id_evento)
        if not evento_existente:
            raise ErrorResponse(404, "Evento não encontrado", {"message": f"Não existe evento com id {id_evento}"})

        eventos_data = data.get("eventos", {}) if isinstance(data, dict) else getattr(data, "eventos", {})

        titulo = (eventos_data.get("titulo", "") if isinstance(eventos_data, dict) else getattr(eventos_data, "titulo", "")).strip()
        descricao = eventos_data.get("descricao") if isinstance(eventos_data, dict) else getattr(eventos_data, "descricao", None)

        data_evento_str = (eventos_data.get("dataEvento") or eventos_data.get("data_evento")) if isinstance(eventos_data, dict) else \
                         (getattr(eventos_data, "dataEvento", None) or getattr(eventos_data, "data_evento", None))

        local_evento = (eventos_data.get("localEvento") or eventos_data.get("local_evento")) if isinstance(eventos_data, dict) else \
                      (getattr(eventos_data, "localEvento", None) or getattr(eventos_data, "local_evento", None))

        limite_vagas = int((eventos_data.get("limiteVagas") or eventos_data.get("limite_vagas", 0)) if isinstance(eventos_data, dict) else \
                         (getattr(eventos_data, "limiteVagas", getattr(eventos_data, "limite_vagas", 0))))

        status_evento = (eventos_data.get("statusEvento") or eventos_data.get("status_evento")) if isinstance(eventos_data, dict) else \
                        (getattr(eventos_data, "statusEvento", getattr(eventos_data, "status_evento", None)))

        if not titulo:
            raise ErrorResponse(400, "Título inválido", {"message": "O título do evento não pode ser vazio."})

        existente = self.eventos_dao.find_by_field("titulo", titulo)
        for evento_mesmo_titulo in existente:
            if evento_mesmo_titulo.get_id_evento() != id_evento:
                raise ErrorResponse(400, "Evento já existe", {"message": f"O evento {titulo} já está cadastrado"})

        if not data_evento_str:
            raise ErrorResponse(400, "Data inválida", {"message": "A data do evento é obrigatória."})

        try:
            data_evento_dt = datetime.strptime(data_evento_str, "%Y-%m-%d")
        except ValueError:
            raise ErrorResponse(400, "Data inválida", {"message": "Formato de data inválido."})

        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if data_evento_dt < hoje:
            raise ErrorResponse(400, "Data inválida", {"message": "A data do evento não pode ser anterior à data atual."})

        if limite_vagas < 0:
            raise ErrorResponse(400, "Limite inválido", {"message": "O limite de vagas deve ser maior ou igual a zero."})

        evento_existente.set_titulo(titulo)
        evento_existente.set_descricao(descricao)
        evento_existente.set_data_evento(data_evento_dt.strftime("%Y-%m-%d"))
        evento_existente.set_local_evento(local_evento)
        evento_existente.set_limite_vagas(limite_vagas)
        evento_existente.set_status_evento(status_evento)

        self.eventos_dao.update(evento_existente)
        return evento_existente

    def delete_service(self, id_evento: int) -> bool:
        logging.info("🟣 EventosService::delete_service")
        evento_existente = self.eventos_dao.find_by_id(id_evento)
        if not evento_existente:
            raise ErrorResponse(404, "Evento não encontrado", {"message": f"Não existe evento com id {id_evento}"})

        return self.eventos_dao.delete(evento_existente)
