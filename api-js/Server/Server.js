const express = require('express');
const MysqlDatabase = require('../Database/MysqlDatabase');
const UsuariosDao = require('../Dao/UsuariosDao');
const MinisterioDao = require('../Dao/MinisterioDao');
const EventosDao = require('../Dao/EventosDao');
const InscricaoDao = require('../Dao/InscricaoDao');
const MensagemDao = require('../Dao/MensagemDao');
const UsuarioMinisterioDao = require('../Dao/UsuarioMinisterioDao');
const UsuariosService = require('../Services/UsuariosService');
const MinisteriosService = require('../Services/MinisteriosService');
const EventosService = require('../Services/EventosService');
const InscricoesService = require('../Services/InscricoesService');
const MensagensService = require('../Services/MensagensService');
const UsuariosController = require('../Controller/UsuariosController');
const MinisteriosController = require('../Controller/MinisteriosController');
const EventosController = require('../Controller/EventosController');
const InscricoesController = require('../Controller/InscricoesController');
const MensagensController = require('../Controller/MensagensController');
const UsuarioMinisterioController = require('../Controller/UsuarioMinisterioController');
const createUsuariosRouter = require('../Router/UsuariosRouter');
const createMinisteriosRouter = require('../Router/MinisteriosRouter');
const createEventosRouter = require('../Router/EventosRouter');
const createInscricoesRouter = require('../Router/InscricoesRouter');
const createMensagensRouter = require('../Router/MensagensRouter');
const createUsuarioMinisterioRouter = require('../Router/UsuarioMinisterioRouter');
const ErrorResponse = require('../Http/ErrorResponse');

function createServer(config = {}) {
  const app = express();
  app.use(express.json());
  app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    if (req.method === 'OPTIONS') return res.sendStatus(204);
    next();
  });

  const db = new MysqlDatabase(config.database || config);
  const usuariosDao = new UsuariosDao(db), ministerioDao = new MinisterioDao(db);
  const eventosDao = new EventosDao(db), inscricaoDao = new InscricaoDao(db);
  const mensagemDao = new MensagemDao(db), usuarioMinisterioDao = new UsuarioMinisterioDao(db);
  const controllers = {
    usuarios: new UsuariosController(new UsuariosService(usuariosDao)),
    ministerios: new MinisteriosController(new MinisteriosService(ministerioDao, usuariosDao)),
    eventos: new EventosController(new EventosService(eventosDao)),
    inscricoes: new InscricoesController(new InscricoesService(inscricaoDao, usuariosDao, eventosDao)),
    mensagens: new MensagensController(new MensagensService(mensagemDao, usuariosDao)),
    usuarioMinisterio: new UsuarioMinisterioController(usuarioMinisterioDao, usuariosDao, ministerioDao)
  };
  app.use(createUsuariosRouter(controllers.usuarios));
  app.use(createMinisteriosRouter(controllers.ministerios));
  app.use(createEventosRouter(controllers.eventos));
  app.use(createInscricoesRouter(controllers.inscricoes));
  app.use(createMensagensRouter(controllers.mensagens));
  app.use(createUsuarioMinisterioRouter(controllers.usuarioMinisterio));
  app.get('/', (req, res) => res.redirect('/login.html'));
  app.use((err, req, res, next) => {
    const status = err instanceof ErrorResponse ? err.getHttpCode() : 500;
    res.status(status).json({ success: false, message: err.message, error: err instanceof ErrorResponse ? (err.getError() || {}) : { code: err.code, stack: err.stack } });
  });
  return app;
}

if (require.main === module) {
  const port = process.env.PORT || 3000;
  createServer().listen(port, () => console.log(`API rodando na porta ${port}`));
}
module.exports = createServer;
