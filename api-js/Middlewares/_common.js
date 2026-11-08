const ErrorResponse = require('../Http/ErrorResponse');
const MeuTokenJWT = require('../Http/MeuTokenJWT');
const fail = (message, detail = message) => { throw new ErrorResponse(400, message, { message: detail }); };
function body(key, fields = []) { return (req, res, next) => { const value = req.body && req.body[key]; if (!value || typeof value !== 'object') return fail('Body invalido', `O JSON deve conter o objeto ${key}`); for (const [field, label] of fields) if (!String(value[field] ?? '').trim()) return fail(`${label} obrigatorio`, `O campo ${key}.${field} e obrigatorio`); next(); }; }
function id(param) { return (req, res, next) => { if (!/^\d+$/.test(String(req.params[param] || ''))) return fail('ID invalido', 'O ID deve ser numerico'); next(); }; }
function token(req, res, next) { const auth = req.headers.authorization || ''; const jwt = new MeuTokenJWT(); if (!jwt.validateToken(auth)) throw new ErrorResponse(401, 'Token invalido', { message: 'Envie um token Bearer valido' }); req.jwtPayload = jwt.getPayload(); req.user = req.jwtPayload.usuario || req.jwtPayload.funcionario || {}; next(); }
function adm(req, res, next) { const p = req.jwtPayload || {}; const u = p.usuario || p.funcionario || {}; const role = String(u.tipoUsuario || u.role || '').trim().toUpperCase(); if (!['ADM', 'ADMIN', 'ADMINISTRADOR', 'ADMINISTRATOR'].includes(role)) throw new ErrorResponse(403, 'Acesso negado', { message: 'Apenas administradores podem executar esta acao' }); next(); }
module.exports = { body, id, token, adm, fail };
