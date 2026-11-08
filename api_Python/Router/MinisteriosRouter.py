from typing import Any
from flask import Flask
from ..Controller.MinisteriosController import MinisteriosController
from ..Middlewares.Ministerios.ValidateMinisteriosBody import validate_ministerios_body
from ..Middlewares.Ministerios.ValidateMinisteriosId import validate_ministerios_id
from ..Middlewares.Usuarios.ValidateUsuariosToken import validate_usuarios_token
from ..Middlewares.Usuarios.ValidateADM import validate_adm

class MinisteriosRouter:
    def __init__(self, app: Flask, ministerios_controller: MinisteriosController):
        self.app = app
        self.controller = ministerios_controller

    def setup_routes(self):
        self.app.add_url_rule("/ministerios", view_func=self.create_route, methods=["POST"])
        self.app.add_url_rule("/ministerios", view_func=self.find_all_route, methods=["GET"])
        self.app.add_url_rule("/ministerios/count", view_func=self.count_route, methods=["GET"])
        self.app.add_url_rule("/ministerios/<int:idMinisterios>", view_func=self.find_by_id_route, methods=["GET"])
        self.app.add_url_rule("/ministerios/<int:idMinisterios>", view_func=self.update_route, methods=["PUT"])
        self.app.add_url_rule("/ministerios/<int:idMinisterios>", view_func=self.delete_route, methods=["DELETE"])

    def create_route(self):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                validate_ministerios_body(req2, lambda req3:
                    self.controller.create_controller(req3))))

    def find_all_route(self):
        from flask import request
        return self.controller.find_all_controller(request)

    def count_route(self):
        from flask import request
        return self.controller.count_controller(request)

    def find_by_id_route(self, idMinisterios):
        from flask import request
        return validate_ministerios_id(request, lambda req:
            self.controller.find_by_id_controller(req, idMinisterios))

    def update_route(self, idMinisterios):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                validate_ministerios_id(req2, lambda req3:
                    validate_ministerios_body(req3, lambda req4:
                        self.controller.update_controller(req4, idMinisterios)))))

    def delete_route(self, idMinisterios):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                validate_ministerios_id(req2, lambda req3:
                    self.controller.delete_controller(req3, idMinisterios))))
