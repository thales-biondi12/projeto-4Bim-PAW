from typing import Any
from flask import Flask
from ..Controller.UsuarioMinisterioController import UsuarioMinisterioController
from ..Middlewares.Usuarios.ValidateUsuariosToken import validate_usuarios_token
from ..Middlewares.Usuarios.ValidateADM import validate_adm

class UsuarioMinisterioRouter:
    def __init__(self, app: Flask, controller: UsuarioMinisterioController):
        self.app = app
        self.controller = controller

    def setup_routes(self):
        self.app.add_url_rule("/usuarios-ministerios", view_func=self.create_route, methods=["POST"])
        self.app.add_url_rule("/usuarios-ministerios", view_func=self.find_all_route, methods=["GET"])
        self.app.add_url_rule("/usuarios-ministerios/count", view_func=self.count_route, methods=["GET"])
        self.app.add_url_rule("/usuarios-ministerios/<int:id>", view_func=self.find_by_id_route, methods=["GET"])
        self.app.add_url_rule("/usuarios-ministerios/<int:id>", view_func=self.update_route, methods=["PUT"])
        self.app.add_url_rule("/usuarios-ministerios/<int:id>", view_func=self.delete_route, methods=["DELETE"])

    def create_route(self):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                self.controller.create(req2)))

    def find_all_route(self):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                self.controller.find_all(req2)))

    def delete_route(self, id):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                self.controller.delete(req2, id)))

    def count_route(self):
        from flask import request
        return validate_usuarios_token(request, lambda req: validate_adm(req, lambda req2: self.controller.count(req2)))

    def find_by_id_route(self, id):
        from flask import request
        return validate_usuarios_token(request, lambda req: validate_adm(req, lambda req2: self.controller.find_by_id(req2, id)))

    def update_route(self, id):
        from flask import request
        return validate_usuarios_token(request, lambda req: validate_adm(req, lambda req2: self.controller.update(req2, id)))
