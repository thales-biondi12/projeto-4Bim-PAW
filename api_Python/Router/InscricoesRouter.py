from typing import Any
from flask import Flask
from ..Controller.InscricoesController import InscricoesController
from ..Middlewares.Inscricao.ValidateInscricoesBody import validate_inscricoes_body
from ..Middlewares.Inscricao.ValidateInscricoesId import validate_inscricoes_id
from ..Middlewares.Inscricao.ValidateInscricoesToken import validate_inscricoes_token
from ..Middlewares.Usuarios.ValidateUsuariosToken import validate_usuarios_token
from ..Middlewares.Usuarios.ValidateADM import validate_adm

class InscricoesRouter:
    def __init__(self, app: Flask, inscricoes_controller: InscricoesController):
        self.app = app
        self.controller = inscricoes_controller

    def setup_routes(self):
        self.app.add_url_rule("/inscricoes", view_func=self.create_route, methods=["POST"])
        self.app.add_url_rule("/inscricoes", view_func=self.find_all_route, methods=["GET"])
        self.app.add_url_rule("/inscricoes/count", view_func=self.count_route, methods=["GET"])
        self.app.add_url_rule("/inscricoes/<int:idInscricoes>", view_func=self.find_by_id_route, methods=["GET"])
        self.app.add_url_rule("/inscricoes/<int:idInscricoes>", view_func=self.update_route, methods=["PUT"])
        self.app.add_url_rule("/inscricoes/<int:idInscricoes>", view_func=self.delete_route, methods=["DELETE"])

    def create_route(self):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_inscricoes_body(req, lambda req2:
                self.controller.create_controller(req2)))

    def find_all_route(self):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                self.controller.find_all_controller(req2)))

    def count_route(self):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                self.controller.count_controller(req2)))

    def find_by_id_route(self, idInscricoes):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                validate_inscricoes_id(req2, lambda req3:
                    self.controller.find_by_id_controller(req3, idInscricoes))))

    def update_route(self, idInscricoes):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                validate_inscricoes_id(req2, lambda req3:
                    validate_inscricoes_body(req3, lambda req4:
                        self.controller.update_controller(req4, idInscricoes)))))

    def delete_route(self, idInscricoes):
        from flask import request
        return validate_usuarios_token(request, lambda req:
            validate_adm(req, lambda req2:
                validate_inscricoes_id(req2, lambda req3:
                    self.controller.delete_controller(req3, idInscricoes))))
