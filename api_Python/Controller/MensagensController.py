import logging
from flask import jsonify, request
from ..Services.MensagensService import MensagensService

class MensagensController:
    def __init__(self, mensagens_service: MensagensService):
        self.mensagens_service = mensagens_service
        logging.info("⬆️ MensagensController::__init__")

    def create_controller(self, req):
        logging.info("🔵 MensagensController::create_controller")
        obj_php = req.get_json()

        payload = getattr(req, "jwt_payload", None)
        if payload:
            # Injeta usuario logado e data atual se faltarem
            mens_data = obj_php.get("mensagens", {})
            if not mens_data.get("usuarioId") and not mens_data.get("usuario_id"):
                usuario = payload.get("usuario", {})
                funcionario = payload.get("funcionario", {})
                mens_data["usuarioId"] = usuario.get("idUsuario") or funcionario.get("idUsuario")

            if not mens_data.get("dataPostagem") and not mens_data.get("data_postagem"):
                from datetime import datetime
                mens_data["dataPostagem"] = datetime.now().strftime("%Y-%m-%d")

            obj_php["mensagens"] = mens_data

        novo_msg = self.mensagens_service.create_service(obj_php)

        return jsonify({
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "mensagens": [novo_msg.to_dict()]
            }
        }), 201

    def find_all_controller(self, req):
        logging.info("🔵 MensagensController::find_all_controller")
        mensagens = self.mensagens_service.find_all_service()

        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {
                "mensagens": [m.to_dict() for m in mensagens]
            }
        }), 200

    def update_controller(self, req, id_mensagens):
        logging.info("🔵 MensagensController::update_controller")
        obj_php = req.get_json()

        msg_atualizada = self.mensagens_service.update_service(id_mensagens, obj_php)

        return jsonify({
            "success": True,
            "message": "Atualização realizada com sucesso",
            "data": {
                "mensagens": [msg_atualizada.to_dict()]
            }
        }), 200

    def delete_controller(self, req, id_mensagens):
        logging.info("🔵 MensagensController::delete_controller")
        deletado = self.mensagens_service.delete_service(id_mensagens)

        if deletado:
            return jsonify({"success": True, "message": "Mensagem deletada com sucesso"}), 200
        return jsonify({"success": False, "message": "Mensagem não encontrada"}), 404

    def count_controller(self, req):
        logging.info("🔵 MensagensController::count_controller")
        total = self.mensagens_service.count_service()

        return jsonify({
            "success": True,
            "message": "Executado com sucesso",
            "data": {"count": total}
        }), 200

    def find_by_id_controller(self, req, id_mensagens):
        logging.info("🔵 MensagensController::find_by_id_controller")
        msg = self.mensagens_service.find_by_id_service(id_mensagens)

        if msg:
            return jsonify({
                "success": True,
                "message": "Busca realizada com sucesso",
                "data": {"mensagens": [msg.to_dict()]}
            }), 200
        return jsonify({"success": False, "message": "Mensagem não encontrada"}), 404
