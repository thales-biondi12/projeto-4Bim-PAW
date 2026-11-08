const body = require('../Middlewares/Usuarios/ValidateUsuariosBody'), login = require('../Middlewares/Usuarios/ValidateUsuariosLoginBody');
const tok = require('../Middlewares/Usuarios/ValidateUsuariosToken'), adm = require('../Middlewares/Usuarios/ValidateADM'), ident = require('../Middlewares/Usuarios/ValidateUsuariosId');
module.exports = c => { const r=require('express').Router(); const b=f=>f.bind(c);
 r.post('/usuarios', body, b(c.createController)); r.post('/usuarios/login', login, b(c.loginController)); r.post('/Usuarios/Login', login, b(c.loginController));
 r.get('/usuarios', tok, adm, b(c.findAllController)); r.get('/usuarios/count', b(c.countController)); r.get('/usuarios/:idUsuario', ident, b(c.findByIdController));
 r.put('/usuarios/:idUsuario', tok, adm, ident, body, b(c.updateController)); r.delete('/usuarios/:idUsuario', tok, adm, ident, b(c.deleteController)); return r; };
