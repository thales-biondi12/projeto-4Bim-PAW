from typing import Any
from flask import Flask
from ..Controller.MensagensController import MensagensController
from ..Middlewares.Mensagens.ValidateMensagensBody import validate_mensagens_body
from ..Middlewares.Mensagens.ValidateMensagensId import validate_mensagens_id
from ..Middlewares.Usuarios.ValidateUsuariosToken import validate_usuarios_token
from ..Middlewares.Usuarios.ValidateADM import validate_adm

class MensagensRouter:
    def __init__(self, app: Flask, mensagens_controller: MensagensController):
        self.app = app
        self.controller = mensagens_controller

    def setup_routes(self):
        self.app.add_url_rule("/mensagens", view_func=self.create_route, methods=["POST"])
        self.app.add_url_rule("/mensagens", view_func=self.find_all_route, methods=["GET"])
        self.app.add_url_rule("/mensagens/count", view_func=self.count_route, methods=["GET"])
        self.app.add_url_rule("/mensagens/<int:idMensagens>", view_func=self.find_by_id_route, methods=["GET"])
        self.app.add_url_rule("/mensagens/<int:idMensagens>", view_func=self.update_route, methods=["PUT"])
        self.app.add_url_rule("/mensagens/<int:idMensagens>", view_func=self.delete_route, methods=["DELETE"])

    def create_route(self):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_mensagens_body(req, lambda req2:
                self.controller.create_controller(req2)))

    def find_all_route(self):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            self.controller.find_all_controller(req))

    def count_route(self):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            self.controller.count_controller(req))

    def find_by_id_route(self, idMensagens):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_mensagens_id(req, lambda req2:
                self.controller.find_by_id_controller(req2, idMensagens)))

    def update_route(self, idMensagens):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                validate_mensagens_id(req2, lambda req3:
                    validate_mensagens_body(req3, lambda req4:
                    self.controller.update_controller(req4, idMensagens)))))

    def delete_route(self, idMensagens):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                validate_mensagens_id(req2, lambda req3:
                    self.controller.delete_controller(req3, idMensagens))))
