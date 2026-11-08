import logging
from flask import jsonify, request
from ..Services.UsuariosService import UsuariosService
from ..Http.MeuTokenJWT import MeuTokenJWT

class UsuariosController:
    def __init__(self, usuarios_service: UsuariosService):
        self.usuarios_service = usuarios_service
        logging.info("⬆️ UsuariosController::__init__")

    def create_controller(self, req):
        logging.info("🔵 UsuariosController::create_controller")
        obj_php = req.get_json()

        novo_usuario = self.usuarios_service.create_service(obj_php)

        return jsonify({
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "usuarios": [novo_usuario.to_dict()]
            }
        }), 201

    def login_controller(self, req):
        logging.info("🔵 UsuariosController::login_controller")
        obj_php = req.get_json()

        usuario = self.usuarios_service.login_service(obj_php)

        jwt = MeuTokenJWT()
        # Claims para o token
        claims = {
            "idUsuario": usuario.get_id_usuario(),
            "nomeUsuario": usuario.get_nome_usuario(),
            "email": usuario.get_email(),
            "tipoUsuario": usuario.get_tipo_usuario(),
            # Legado
            "idFuncionario": usuario.get_id_usuario(),
            "name": usuario.get_nome_usuario(),
            "role": usuario.get_tipo_usuario(),
        }

        # No Python, passamos o dict de claims diretamente
        token = jwt.gerar_token(type('Claims', (object,), claims))

        return jsonify({
            "success": True,
            "message": "Login realizado com sucesso",
            "data": {
                "token": token,
                "token_type": "Bearer",
                "expires_in": jwt.get_duration(),
                "usuario": {
                    "idUsuario": usuario.get_id_usuario(),
                    "nomeUsuario": usuario.get_nome_usuario(),
                    "email": usuario.get_email(),
                    "tipoUsuario": usuario.get_tipo_usuario(),
                }
            }
        }), 200

    def find_all_controller(self, req):
        logging.info("🔵 UsuariosController::find_all_controller")
        usuarios = self.usuarios_service.find_all_service()

        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {
                "usuarios": [u.to_dict() for u in usuarios]
            }
        }), 200

    def find_by_id_controller(self, req, id_usuario):
        logging.info("🔵 UsuariosController::find_by_id_controller")
        usuario = self.usuarios_service.find_by_id_service(id_usuario)

        if usuario:
            return jsonify({
                "success": True,
                "message": "Busca realizada com sucesso",
                "data": {"usuarios": [usuario.to_dict()]}
            }), 200
        return jsonify({"success": False, "message": "Usuario nao encontrado"}), 404

    def update_controller(self, req, id_usuario):
        logging.info("🔵 UsuariosController::update_controller")
        obj_php = req.get_json()

        usuario_atualizado = self.usuarios_service.update_service(id_usuario, obj_php)

        return jsonify({
            "success": True,
            "message": "Atualizacao realizada com sucesso",
            "data": {
                "usuarios": [usuario_atualizado.to_dict()]
            }
        }), 200

    def delete_controller(self, req, id_usuario):
        logging.info("🔵 UsuariosController::delete_controller")
        deletado = self.usuarios_service.delete_service(id_usuario)

        return jsonify({
            "success": deletado,
            "message": "Usuário excluído com sucesso" if deletado else "Usuário não encontrado"
        }), (200 if deletado else 404)

    def count_controller(self, req):
        logging.info("🔵 UsuariosController::count_controller")
        total = self.usuarios_service.count_service()

        return jsonify({
            "success": True,
            "data": {"count": total}
        }), 200
