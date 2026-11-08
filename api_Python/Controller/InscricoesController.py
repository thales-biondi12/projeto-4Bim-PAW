import logging
from flask import jsonify, request
from ..Services.InscricoesService import InscricoesService

class InscricoesController:
    def __init__(self, inscricoes_service: InscricoesService):
        self.inscricoes_service = inscricoes_service
        logging.info("⬆️ InscricoesController::__init__")

    def create_controller(self, req):
        logging.info("🔵 InscricoesController::create_controller")
        obj_php = req.get_json()

        # Injeta usuario logado se não enviado (via middleware payload)
        payload = getattr(req, "jwt_payload", None)
        if payload and not (obj_php.get("inscricoes", {}).get("usuarioId")):
            usuario = payload.get("usuario", {})
            funcionario = payload.get("funcionario", {})
            obj_php.setdefault("inscricoes", {})["usuarioId"] = usuario.get("idUsuario") or funcionario.get("idUsuario")

        novo_insc = self.inscricoes_service.create_service(obj_php)

        return jsonify({
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "inscricoes": [
                    {
                        "idInscricoes": novo_insc.get_id_inscricoes(),
                        "usuarioId": novo_insc.get_usuario_id(),
                        "eventoId": novo_insc.get_evento_id(),
                        "dataInscricao": novo_insc.get_data_inscricao(),
                        "presenca": novo_insc.get_presenca(),
                    }
                ]
            }
        }), 201

    def find_all_controller(self, req):
        logging.info("🔵 InscricoesController::find_all_controller")
        inscricoes = self.inscricoes_service.find_all_service()

        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {
                "inscricoes": [i.to_dict() for i in inscricoes]
            }
        }), 200

    def update_controller(self, req, id_inscricoes):
        logging.info("🔵 InscricoesController::update_controller")
        obj_php = req.get_json()

        insc_atualizada = self.inscricoes_service.update_service(id_inscricoes, obj_php)

        return jsonify({
            "success": True,
            "message": "Atualização realizada com sucesso",
            "data": {
                "inscricoes": [insc_atualizada.to_dict()]
            }
        }), 200

    def delete_controller(self, req, id_inscricoes):
        logging.info("🔵 InscricoesController::delete_controller")
        deletado = self.inscricoes_service.delete_service(id_inscricoes)

        if deletado:
            return jsonify({"success": True, "message": "Inscrição deletada com sucesso"}), 200
        return jsonify({"success": False, "message": "Inscrição não encontrada"}), 404

    def count_controller(self, req):
        logging.info("🔵 InscricoesController::count_controller")
        total = self.inscricoes_service.count_service()

        return jsonify({
            "success": True,
            "message": "Executado com sucesso",
            "data": {"count": total}
        }), 200

    def find_by_id_controller(self, req, id_inscricoes):
        logging.info("🔵 InscricoesController::find_by_id_controller")
        insc = self.inscricoes_service.find_by_id_service(id_inscricoes)

        if insc:
            return jsonify({
                "success": True,
                "message": "Busca realizada com sucesso",
                "data": {"inscricoes": [insc.to_dict()]}
            }), 200
        return jsonify({"success": False, "message": "Inscrição não encontrada"}), 404
