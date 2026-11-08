const tok=require('../Middlewares/Usuarios/ValidateUsuariosToken'),adm=require('../Middlewares/Usuarios/ValidateADM');
module.exports=c=>{const r=require('express').Router(),b=f=>f.bind(c); r.post('/usuarios-ministerios',tok,adm,b(c.create)); r.get('/usuarios-ministerios',tok,adm,b(c.findAll)); r.delete('/usuarios-ministerios/:id',tok,adm,b(c.delete)); return r;};
