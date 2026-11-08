from typing import Any
from flask import Flask
from ..Controller.UsuariosController import UsuariosController
from ..Middlewares.Usuarios.ValidateUsuariosBody import validate_usuarios_body
from ..Middlewares.Usuarios.ValidateUsuariosId import validate_usuarios_id
from ..Middlewares.Usuarios.ValidateUsuariosLoginBody import validate_usuarios_login_body
from ..Middlewares.Usuarios.ValidateUsuariosToken import validate_usuarios_token
from ..Middlewares.Usuarios.ValidateADM import validate_adm

class UsuariosRouter:
    def __init__(self, app: Flask, usuarios_controller: UsuariosController):
        self.app = app
        self.controller = usuarios_controller

    def setup_routes(self):
        self.app.add_url_rule("/usuarios", view_func=self.create_route, methods=["POST"])
        self.app.add_url_rule("/usuarios/login", view_func=self.login_route, methods=["POST"])
        self.app.add_url_rule("/Usuarios/Login", view_func=self.login_route, methods=["POST"])
        self.app.add_url_rule("/usuarios", view_func=self.find_all_route, methods=["GET"])
        self.app.add_url_rule("/usuarios/count", view_func=self.count_route, methods=["GET"])
        self.app.add_url_rule("/usuarios/<int:idUsuario>", view_func=self.find_by_id_route, methods=["GET"])
        self.app.add_url_rule("/usuarios/<int:idUsuario>", view_func=self.update_route, methods=["PUT"])
        self.app.add_url_rule("/usuarios/<int:idUsuario>", view_func=self.delete_route, methods=["DELETE"])

    def create_route(self):
        from flask import request
        return validate_usuarios_body(request, lambda req:
            self.controller.create_controller(req))

    def login_route(self):
        from flask import request
        return validate_usuarios_login_body(request, lambda req:
            self.controller.login_controller(req))

    def find_all_route(self):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                self.controller.find_all_controller(req2)))

    def count_route(self):
        from flask import request
        return self.controller.count_controller(request)

    def find_by_id_route(self, idUsuario):
        from flask import request
        return validate_usuarios_id(request, lambda req:
            self.controller.find_by_id_controller(req, idUsuario))

    def update_route(self, idUsuario):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                validate_usuarios_id(req2, lambda req3:
                    validate_usuarios_body(req3, lambda req4:
                        self.controller.update_controller(req4, idUsuario), require_password=False))))

    def delete_route(self, idUsuario):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                validate_usuarios_id(req2, lambda req3:
                    self.controller.delete_controller(req3, idUsuario))))
