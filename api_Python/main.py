import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

# O diretório original usa hífen no nome; o alias permite imports relativos.
import types
package = types.ModuleType("api_python")
package.__path__ = [str(ROOT)]
sys.modules.setdefault("api_python", package)

from flask import Flask
from api_python.Database.MysqlDatabase import MysqlDatabase
from api_python.Dao.UsuariosDao import UsuariosDao
from api_python.Dao.MinisterioDao import MinisterioDao
from api_python.Dao.EventosDao import EventosDao
from api_python.Dao.InscricaoDao import InscricaoDao
from api_python.Dao.MensagemDao import MensagemDao
from api_python.Dao.UsuarioMinisterioDao import UsuarioMinisterioDao
from api_python.Services.UsuariosService import UsuariosService
from api_python.Services.MinisteriosService import MinisteriosService
from api_python.Services.EventosService import EventosService
from api_python.Services.InscricoesService import InscricoesService
from api_python.Services.MensagensService import MensagensService
from api_python.Controller.UsuariosController import UsuariosController
from api_python.Controller.MinisteriosController import MinisteriosController
from api_python.Controller.EventosController import EventosController
from api_python.Controller.InscricoesController import InscricoesController
from api_python.Controller.MensagensController import MensagensController
from api_python.Controller.UsuarioMinisterioController import UsuarioMinisterioController
from api_python.Router.UsuariosRouter import UsuariosRouter
from api_python.Router.MinisteriosRouter import MinisteriosRouter
from api_python.Router.EventosRouter import EventosRouter
from api_python.Router.InscricoesRouter import InscricoesRouter
from api_python.Router.MensagensRouter import MensagensRouter
from api_python.Router.UsuarioMinisterioRouter import UsuarioMinisterioRouter
from api_python.Server.Server import Server


def create_app(config=None):
    # Serve o frontend da pasta public junto com a API Python.
    app = Flask(__name__, static_folder=str(PARENT / "public"), static_url_path="")
    db = MysqlDatabase(config or {})
    usuarios = UsuariosDao(db)
    ministerios = MinisterioDao(db)
    eventos = EventosDao(db)
    inscricoes = InscricaoDao(db)
    mensagens = MensagemDao(db)
    vinculos = UsuarioMinisterioDao(db)
    routers = [
        UsuariosRouter(app, UsuariosController(UsuariosService(usuarios))),
        MinisteriosRouter(app, MinisteriosController(MinisteriosService(ministerios, usuarios))),
        EventosRouter(app, EventosController(EventosService(eventos))),
        InscricoesRouter(app, InscricoesController(InscricoesService(inscricoes, usuarios, eventos))),
        MensagensRouter(app, MensagensController(MensagensService(mensagens, usuarios))),
        UsuarioMinisterioRouter(app, UsuarioMinisterioController(vinculos, usuarios, ministerios)),
    ]
    return Server(*routers, app=app).app


app = create_app()

if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "5000")), debug=False)
