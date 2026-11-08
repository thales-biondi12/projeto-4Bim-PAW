const UsuarioMinisterioDao = require('../Dao/UsuarioMinisterioDao');
const UsuariosDao = require('../Dao/UsuariosDao');
const MinisterioDao = require('../Dao/MinisterioDao');
const UsuarioMinisterio = require('../Models/UsuarioMinisterio');

class UsuarioMinisterioController {
    constructor(usuarioMinisterioDao, uDao, mDao) {
        this.dao = usuarioMinisterioDao;
        this.uDao = uDao;
        this.mDao = mDao;
    }

    async create(req, res) {
        const objJS = req.body;
        const uid = objJS.inscricao?.idUsuario || objJS.idUsuario;
        const mid = objJS.inscricao?.idMinisterio || objJS.idMinisterio;
        const funcao = objJS.inscricao?.funcao || objJS.funcao || "Membro";
        const dataEntrada = objJS.inscricao?.dataEntrada || new Date().toISOString().split('T')[0];

        if (!uid || !mid) {
            return res.status(400).json({
                success: false,
                message: "idUsuario e idMinisterio obrigatórios"
            });
        }

        if (!(await this.uDao.findById(parseInt(uid)))) {
            return res.status(400).json({
                success: false,
                message: "Usuário não encontrado"
            });
        }

        if (!(await this.mDao.findById(parseInt(mid)))) {
            return res.status(400).json({
                success: false,
                message: "Ministério não encontrado"
            });
        }

        if (await this.dao.exists(parseInt(uid), parseInt(mid))) {
            return res.status(400).json({
                success: false,
                message: "Usuário já está neste ministério"
            });
        }

        const novoVinculo = new UsuarioMinisterio();
        novoVinculo.setIdUsuario(parseInt(uid));
        novoVinculo.setIdMinisterio(parseInt(mid));
        novoVinculo.setFuncao(funcao);
        novoVinculo.setDataEntrada(dataEntrada);

        const vinculoCriado = await this.dao.create(novoVinculo);

        return res.status(201).json({
            success: true,
            data: vinculoCriado.toJSON()
        });
    }

    async findAll(req, res) {
        const list = await this.dao.findAll();
        return res.status(200).json({
            success: true,
            data: {
                vinculos: list.map(v => v.toJSON())
            }
        });
    }
    async findById(req,res) { const v=await this.dao.findById(req.params.id); if(!v)return res.status(404).json({success:false}); return res.json({success:true,data:{vinculo:v.toJSON()}}); }
    async count(req,res) { return res.json({success:true,data:{count:await this.dao.count()}}); }
    async update(req,res) { const v=await this.dao.findById(req.params.id); if(!v)return res.status(404).json({success:false}); const b=req.body||{}; const u=Number(b.idUsuario??v.getIdUsuario()),m=Number(b.idMinisterio??v.getIdMinisterio()); if(!(await this.uDao.findById(u))||!(await this.mDao.findById(m)))return res.status(400).json({success:false,message:'Usuário ou ministério não encontrado'}); if(await this.dao.existsOther(u,m,Number(req.params.id)))return res.status(400).json({success:false,message:'Vínculo duplicado'}); v.setIdUsuario(u);v.setIdMinisterio(m);v.setDataEntrada(b.dataEntrada??v.getDataEntrada());v.setFuncao(b.funcao??v.getFuncao());await this.dao.update(v);return res.json({success:true,data:{vinculo:v.toJSON()}}); }

    async delete(req, res) {
        const id = parseInt(req.params.id);
        const ok = await this.dao.delete(id);

        if (ok) {
            return res.status(200).json({ success: true });
        } else {
            return res.status(404).json({ success: false });
        }
    }
}

module.exports = UsuarioMinisterioController;
