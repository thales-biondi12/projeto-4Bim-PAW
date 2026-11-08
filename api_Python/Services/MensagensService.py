import logging
from datetime import datetime
from typing import List, Optional, Any
from ..Models.Mensagens import Mensagens
from ..Dao.MensagemDao import MensagemDao
from ..Dao.UsuariosDao import UsuariosDao
from ..Http.ErrorResponse import ErrorResponse

class MensagensService:
    def __init__(self, mensagem_dao_dep: MensagemDao, usuarios_dao_dep: UsuariosDao):
        self.mensagem_dao = mensagem_dao_dep
        self.usuarios_dao = usuarios_dao_dep
        logging.info("⬆️ MensagensService::__init__")

    def create_service(self, data: Any) -> Mensagens:
        logging.info("🟣 MensagensService::create_service")

        mens_data = data.get("mensagens", {}) if isinstance(data, dict) else getattr(data, "mensagens", {})

        titulo = (mens_data.get("titulo", "") if isinstance(mens_data, dict) else getattr(mens_data, "titulo", "")).strip()
        conteudo = (mens_data.get("conteudo", "") if isinstance(mens_data, dict) else getattr(mens_data, "conteudo", "")).strip()
        usuario_id = (mens_data.get("usuarioId") if isinstance(mens_data, dict) else getattr(mens_data, "usuarioId", None))
        data_postagem = (mens_data.get("dataPostagem") if isinstance(mens_data, dict) else getattr(mens_data, "dataPostagem", None))

        if not titulo:
            raise ErrorResponse(400, "Título inválido", {"message": "O título da mensagem não pode ser vazio."})
        if not conteudo:
            raise ErrorResponse(400, "Conteúdo inválido", {"message": "O conteúdo da mensagem não pode ser vazio."})
        if not usuario_id or not self.usuarios_dao.find_by_id(usuario_id):
            raise ErrorResponse(400, "Usuário não encontrado", {"message": f"O usuário com id {usuario_id} não existe."})

        if not data_postagem:
            data_postagem = datetime.now().strftime("%Y-%m-%d")

        mensagem = Mensagens()
        mensagem.set_titulo(titulo)
        mensagem.set_conteudo(conteudo)
        mensagem.set_usuario_id(usuario_id)
        mensagem.set_data_postagem(data_postagem)

        return self.mensagem_dao.create(mensagem)

    def count_service(self) -> int:
        logging.info("🟣 MensagensService::count_service")
        return self.mensagem_dao.count()

    def find_all_service(self) -> List[Mensagens]:
        logging.info("🟣 MensagensService::find_all_service")
        return self.mensagem_dao.find_all()

    def find_by_id_service(self, id_mensagens: int) -> Optional[Mensagens]:
        logging.info("🟣 MensagensService::find_by_id_service")
        return self.mensagem_dao.find_by_id(id_mensagens)

    def update_service(self, id_mensagens: int, data: Any) -> Mensagens:
        logging.info("🟣 MensagensService::update_service")

        mensagem_existente = self.mensagem_dao.find_by_id(id_mensagens)
        if not mensagem_existente:
            raise ErrorResponse(404, "Mensagem não encontrada", {"message": f"Não existe mensagem com id {id_mensagens}"})

        mens_data = data.get("mensagens", {}) if isinstance(data, dict) else getattr(data, "mensagens", {})

        titulo = (mens_data.get("titulo", "") if isinstance(mens_data, dict) else getattr(mens_data, "titulo", "")).strip()
        conteudo = (mens_data.get("conteudo", "") if isinstance(mens_data, dict) else getattr(mens_data, "conteudo", "")).strip()
        usuario_id = (mens_data.get("usuarioId") if isinstance(mens_data, dict) else getattr(mens_data, "usuarioId", None))
        data_postagem = (mens_data.get("dataPostagem") if isinstance(mens_data, dict) else getattr(mens_data, "dataPostagem", None))

        if not titulo:
            raise ErrorResponse(400, "Título inválido", {"message": "O título da mensagem não pode ser vazio."})
        if not conteudo:
            raise ErrorResponse(400, "Conteúdo inválido", {"message": "O conteúdo da mensagem não pode ser vazio."})
        if not usuario_id or not self.usuarios_dao.find_by_id(usuario_id):
            raise ErrorResponse(400, "Usuário não encontrado", {"message": f"O usuário com id {usuario_id} não existe."})

        mensagem_existente.set_titulo(titulo)
        mensagem_existente.set_conteudo(conteudo)
        mensagem_existente.set_usuario_id(usuario_id)
        mensagem_existente.set_data_postagem(data_postagem)

        self.mensagem_dao.update(mensagem_existente)
        return mensagem_existente

    def delete_service(self, id_mensagens: int) -> bool:
        logging.info("🟣 MensagensService::delete_service")
        mensagem_existente = self.mensagem_dao.find_by_id(id_mensagens)
        if not mensagem_existente:
            raise ErrorResponse(404, "Mensagem não encontrada", {"message": f"Não existe mensagem com id {id_mensagens}"})

        return self.mensagem_dao.delete(mensagem_existente)
