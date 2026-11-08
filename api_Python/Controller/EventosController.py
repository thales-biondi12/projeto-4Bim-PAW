import logging
from flask import jsonify, request
from ..Services.EventosService import EventosService

class EventosController:
    def __init__(self, eventos_service: EventosService):
        self.eventos_service = eventos_service
        logging.info("⬆️ EventosController::__init__")

    def create_controller(self, req):
        logging.info("🔵 EventosController::create_controller")
        obj_php = req.get_json()

        novo_evento = self.eventos_service.create_service(obj_php)

        return jsonify({
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "eventos": [
                    {
                        "idEvento": novo_evento.get_id_evento(),
                        "titulo": novo_evento.get_titulo(),
                        "descricao": novo_evento.get_descricao(),
                        "dataEvento": novo_evento.get_data_evento(),
                        "localEvento": novo_evento.get_local_evento(),
                        "limiteVagas": novo_evento.get_limite_vagas(),
                        "statusEvento": novo_evento.get_status_evento(),
                    }
                ]
            }
        }), 201

    def find_all_controller(self, req):
        logging.info("🔵 EventosController::find_all_controller")
        eventos = self.eventos_service.find_all_service()

        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {
                "eventos": [e.to_dict() for e in eventos]
            }
        }), 200

    def update_controller(self, req, id_evento):
        logging.info("🔵 EventosController::update_controller")
        obj_php = req.get_json()

        evento_atualizado = self.eventos_service.update_service(id_evento, obj_php)

        return jsonify({
            "success": True,
            "message": "Atualização realizada com sucesso",
            "data": {
                "eventos": [evento_atualizado.to_dict()]
            }
        }), 200

    def delete_controller(self, req, id_evento):
        logging.info("🔵 EventosController::delete_controller")
        deletado = self.eventos_service.delete_service(id_evento)

        if deletado:
            return jsonify({"success": True, "message": "Evento deletado com sucesso"}), 200
        return jsonify({"success": False, "message": "Evento não encontrado"}), 404

    def count_controller(self, req):
        logging.info("🔵 EventosController::count_controller")
        total = self.eventos_service.count_service()

        return jsonify({
            "success": True,
            "message": "Executado com sucesso",
            "data": {"count": total}
        }), 200

    def find_by_id_controller(self, req, id_evento):
        logging.info("🔵 EventosController::find_by_id_controller")
        evento = self.eventos_service.find_by_id_service(id_evento)

        if evento:
            return jsonify({
                "success": True,
                "message": "Busca realizada com sucesso",
                "data": {"eventos": [evento.to_dict()]}
            }), 200
        return jsonify({"success": False, "message": "Evento não encontrado"}), 404
