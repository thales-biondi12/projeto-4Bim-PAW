from typing import List, Any
from flask import Flask
from ..Controller.EventosController import EventosController
from ..Middlewares.Eventos.ValidateEventosBody import validate_eventos_body
from ..Middlewares.Eventos.ValidateEventosId import validate_eventos_id

class EventosRouter:
    def __init__(self, app: Flask, eventos_controller: EventosController):
        self.app = app
        self.controller = eventos_controller

    def setup_routes(self):
        # POST /eventos
        self.app.add_url_rule(
            "/eventos",
            view_func=self.create_route,
            methods=["POST"]
        )
        # GET /eventos
        self.app.add_url_rule(
            "/eventos",
            view_func=self.find_all_route,
            methods=["GET"]
        )
        # GET /eventos/count
        self.app.add_url_rule(
            "/eventos/count",
            view_func=self.count_route,
            methods=["GET"]
        )
        # GET /eventos/<idEvento>
        self.app.add_url_rule(
            "/eventos/<int:idEvento>",
            view_func=self.find_by_id_route,
            methods=["GET"]
        )
        # PUT /eventos/<idEvento>
        self.app.add_url_rule(
            "/eventos/<int:idEvento>",
            view_func=self.update_route,
            methods=["PUT"]
        )
        # DELETE /eventos/<idEvento>
        self.app.add_url_rule(
            "/eventos/<int:idEvento>",
            view_func=self.delete_route,
            methods=["DELETE"]
        )

    def create_route(self):
        from flask import request
        return validate_eventos_body(request, lambda req: self.controller.create_controller(req))

    def find_all_route(self):
        from flask import request
        return self.controller.find_all_controller(request)

    def count_route(self):
        from flask import request
        return self.controller.count_controller(request)

    def find_by_id_route(self, idEvento):
        from flask import request
        return validate_eventos_id(request, lambda req: self.controller.find_by_id_controller(req, idEvento))

    def update_route(self, idEvento):
        from flask import request
        # A ordem dos middlewares importa
        return validate_eventos_body(request, lambda req:
            validate_eventos_id(req, lambda req2:
                self.controller.update_controller(req2, idEvento)))

    def delete_route(self, idEvento):
        from flask import request
        return validate_eventos_id(request, lambda req: self.controller.delete_controller(req, idEvento))
