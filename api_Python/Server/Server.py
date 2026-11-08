import logging
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from ..Router.UsuariosRouter import UsuariosRouter
from ..Router.MinisteriosRouter import MinisteriosRouter
from ..Router.EventosRouter import EventosRouter
from ..Router.InscricoesRouter import InscricoesRouter
from ..Router.MensagensRouter import MensagensRouter
from ..Router.UsuarioMinisterioRouter import UsuarioMinisterioRouter
from ..Http.ErrorResponse import ErrorResponse

class Server:
    """
    Classe Server - Responsável por configurar e executar o servidor HTTP Flask.
    """
    def __init__(self,
                 usuarios_router: UsuariosRouter,
                 ministerios_router: MinisteriosRouter,
                 eventos_router: EventosRouter,
                 inscricoes_router: InscricoesRouter,
                 mensagens_router: MensagensRouter,
                 usuario_ministerio_router: UsuarioMinisterioRouter,
                 app=None):

        self.app = app or Flask(__name__)

        # Configuração de CORS (equivalente ao middleware de OPTIONS do Slim)
        CORS(self.app, resources={r"/*": {"origins": "*"}})

        self.usuarios_router = usuarios_router
        self.ministerios_router = ministerios_router
        self.eventos_router = eventos_router
        self.inscricoes_router = inscricoes_router
        self.mensagens_router = mensagens_router
        self.usuario_ministerio_router = usuario_ministerio_router

        self._setup_routes()
        self._setup_error_handling()

    def _setup_routes(self):
        """
        Configura as rotas da aplicação.
        """
        routers = [self.usuarios_router, self.ministerios_router, self.eventos_router,
                   self.inscricoes_router, self.mensagens_router, self.usuario_ministerio_router]
        for router in routers:
            for name in ("create_route", "login_route", "find_all_route", "count_route",
                         "find_by_id_route", "update_route", "delete_route"):
                handler = getattr(router, name, None)
                if handler is not None:
                    def endpoint(*args, _handler=handler, **kwargs):
                        return _handler(*args, **kwargs)
                    endpoint.__name__ = f"{router.__class__.__name__}_{name}"
                    setattr(router, name, endpoint)

        self.usuarios_router.setup_routes()
        self.ministerios_router.setup_routes()
        self.eventos_router.setup_routes()
        self.inscricoes_router.setup_routes()
        self.mensagens_router.setup_routes()
        self.usuario_ministerio_router.setup_routes()

        # Rota Raiz
        @self.app.route("/")
        def index():
            return redirect("/login.html", code=302)

    def _setup_error_handling(self):
        """
        Tratamento global de erros para padronizar a resposta JSON.
        """
        @self.app.errorhandler(Exception)
        def handle_exception(e):
            # Se for um erro personalizado ErrorResponse
            if isinstance(e, ErrorResponse):
                payload = {
                    "success": False,
                    "message": str(e),
                    "error": e.get_error() if e.get_error() else {}
                }
                status_code = e.get_http_code()
            else:
                # Erro genérico do sistema
                payload = {
                    "success": False,
                    "message": str(e),
                    "error": {
                        "type": type(e).__name__,
                        "details": "Internal Server Error"
                    }
                }
                status_code = 500

            return jsonify(payload), status_code

    def run(self, host="0.0.0.0", port=5000, debug=True):
        """
        Executa o servidor Flask.
        """
        logging.info(f"🚀 Servidor iniciando em http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug)
