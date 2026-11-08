import logging
from flask import jsonify, request
from ..Services.MinisteriosService import MinisteriosService

class MinisteriosController:
    def __init__(self, ministerios_service: MinisteriosService):
        self.ministerios_service = ministerios_service
        logging.info("⬆️ MinisteriosController::__init__")

    def create_controller(self, req):
        logging.info("🔵 MinisteriosController::create_controller")
        obj_php = req.get_json()

        novo_min = self.ministerios_service.create_service(obj_php)

        return jsonify({
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "ministerios": [novo_min.to_dict()]
            }
        }), 201

    def find_all_controller(self, req):
        logging.info("🔵 MinisteriosController::find_all_controller")
        ministerios = self.ministerios_service.find_all_service()

        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {
                "ministerios": [m.to_dict() for m in ministerios]
            }
        }), 200

    def find_by_id_controller(self, req, id_ministerios):
        logging.info("🔵 MinisteriosController::find_by_id_controller")
        min_res = self.ministerios_service.find_by_id_service(id_ministerios)

        if min_res:
            return jsonify({
                "success": True,
                "message": "Busca realizada com sucesso",
                "data": {"ministerios": [min_res.to_dict()]}
            }), 200
        return jsonify({"success": False, "message": "Ministério não encontrado"}), 404

    def update_controller(self, req, id_ministerios):
        logging.info("🔵 MinisteriosController::update_controller")
        obj_php = req.get_json()

        min_atualizado = self.ministerios_service.update_service(id_ministerios, obj_php)

        return jsonify({
            "success": True,
            "message": "Atualização realizada com sucesso",
            "data": {
                "ministerios": [min_atualizado.to_dict()]
            }
        }), 200

    def delete_controller(self, req, id_ministerios):
        logging.info("🔵 MinisteriosController::delete_controller")
        deletado = self.ministerios_service.delete_service(id_ministerios)

        if deletado:
            return jsonify({"success": True, "message": "Ministério deletado com sucesso"}), 200
        return jsonify({"success": False, "message": "Ministério não encontrado"}), 404

    def count_controller(self, req):
        logging.info("🔵 MinisteriosController::count_controller")
        total = self.ministerios_service.count_service()

        return jsonify({
            "success": True,
            "message": "Executado com sucesso",
            "data": {"count": total}
        }), 200
