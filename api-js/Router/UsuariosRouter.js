const body = require('../Middlewares/Usuarios/ValidateUsuariosBody'), login = require('../Middlewares/Usuarios/ValidateUsuariosLoginBody');
const commonBody = require('../Middlewares/_common').body;
const tok = require('../Middlewares/Usuarios/ValidateUsuariosToken'), adm = require('../Middlewares/Usuarios/ValidateADM'), ident = require('../Middlewares/Usuarios/ValidateUsuariosId');
module.exports = c => { const r=require('express').Router(); const b=f=>f.bind(c);
 const safe=f=>(req,res,next)=>Promise.resolve(f.call(c,req,res,next)).catch(next); r.post('/usuarios', body, safe(c.createController)); r.post('/usuarios/login', login, safe(c.loginController)); r.post('/Usuarios/Login', login, safe(c.loginController));
 r.get('/usuarios', tok, adm, safe(c.findAllController)); r.get('/usuarios/count', safe(c.countController)); r.get('/usuarios/:idUsuario', ident, safe(c.findByIdController));
 const updateBody = commonBody('usuarios', [['nomeUsuario','Nome'],['email','Email']], { requirePassword: false });
 r.put('/usuarios/:idUsuario', tok, adm, ident, updateBody, safe(c.updateController)); r.delete('/usuarios/:idUsuario', tok, adm, ident, safe(c.deleteController)); return r; };
