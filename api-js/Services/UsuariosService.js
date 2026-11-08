const Usuarios = require('../Models/Usuarios');
const UsuariosDao = require('../Dao/UsuariosDao');
const ErrorResponse = require('../Http/ErrorResponse');
const bcrypt = require('bcrypt');
const crypto = require('crypto');

class UsuariosService {
    constructor(usuariosDAODependency) {
        console.log("⬆️ UsuariosService::__construct()");
        this.usuariosDAO = usuariosDAODependency;
    }

    async createService(objJS) {
        console.log("🟣 UsuariosService::createService()");

        const usuario = new Usuarios();
        const dados = objJS.usuarios || objJS.usuario || null;
        if (!dados) {
            throw new ErrorResponse(400, "Dados inválidos", {
                message: "Objeto 'usuarios' é obrigatório",
            });
        }

        usuario.setNomeUsuario(dados.nomeUsuario || dados.nome || "");
        usuario.setEmail(dados.email);

        const senhaPura = dados.senha;
        const senhaHash = await bcrypt.hash(senhaPura, 10);
        usuario.setSenha(senhaHash);

        usuario.setTel(dados.tel || null);
        usuario.setTipoUsuario(dados.tipoUsuario || dados.tipo_usuario || "MEMBRO");
        usuario.setDataNasc(dados.data_nasc || dados.dataNasc || null);

        const resultado = await this.usuariosDAO.findByField("email", usuario.getEmail());
        if (resultado && resultado.length > 0) {
            throw new ErrorResponse(400, "Usuário já existe", {
                message: `O email ${usuario.getEmail()} já está cadastrado`,
            });
        }

        return await this.usuariosDAO.create(usuario);
    }

    async loginService(objJS) {
        console.log("🟣 UsuariosService::loginService()");

        const dados = objJS.usuarios || objJS.usuario || objJS.funcionario || null;

        if (!dados || !dados.email || !dados.senha) {
            throw new ErrorResponse(400, "Dados inválidos", {
                message: "Email e senha são obrigatórios",
            });
        }

        const email = (dados.email).trim();
        const senhaInformada = String(dados.senha);

        const resultado = await this.usuariosDAO.findByField("email", email);
        if (!resultado || resultado.length === 0) {
            throw new ErrorResponse(401, "Credenciais inválidas", {
                message: "Email ou senha incorretos",
            });
        }

        const usuario = resultado[0];
        // O MySQL pode devolver senhas legadas numéricas como number.
        const senhaBanco = String(usuario.getSenha());

        // No Node.js, usamos bcrypt.compare para verificar senhas hasheadas
        // Se a senha no banco for texto puro (legado), fazemos comparação simples
        let senhaValida = false;

        // Heurística simples para detectar se é hash bcrypt (geralmente começa com $2a$, $2b$ ou $2y$)
        const isHashed = senhaBanco.startsWith('$2a$') || senhaBanco.startsWith('$2b$') || senhaBanco.startsWith('$2y$');

        if (isHashed) {
            senhaValida = await bcrypt.compare(senhaInformada, senhaBanco);
        } else if (/^[a-f0-9]{64}$/i.test(String(senhaBanco))) {
            const sha256 = crypto.createHash('sha256').update(senhaInformada).digest('hex');
            senhaValida = sha256 === String(senhaBanco);
            if (senhaValida) {
                usuario.setSenha(await bcrypt.hash(senhaInformada, 10));
                await this.usuariosDAO.update(usuario);
            }
        } else {
            // Compatibilidade com senhas legadas em texto puro
            senhaValida = (senhaBanco === String(senhaInformada));
            if (senhaValida) {
                // Migra automaticamente para hash
                const novoHash = await bcrypt.hash(senhaInformada, 10);
                usuario.setSenha(novoHash);
                await this.usuariosDAO.update(usuario);
            }
        }

        if (!senhaValida) {
            throw new ErrorResponse(401, "Credenciais inválidas", {
                message: "Email ou senha incorretos",
            });
        }

        return usuario;
    }

    async countService() {
        console.log("🟣 UsuariosService::countService()");
        return await this.usuariosDAO.count();
    }

    async findAllService() {
        console.log("🟣 UsuariosService::findAllService()");
        return await this.usuariosDAO.findAll();
    }

    async findByIdService(idUsuario) {
        console.log("🟣 UsuariosService::findByIdService()");
        return await this.usuariosDAO.findById(idUsuario);
    }

    async updateService(idUsuario, objJS) {
        console.log("🟣 UsuariosService::updateService()");

        const usuarioExistente = await this.usuariosDAO.findById(idUsuario);
        if (!usuarioExistente) {
            throw new ErrorResponse(404, "Usuário não encontrado", {
                message: `Não existe usuário com id ${idUsuario}`,
            });
        }

        const dados = objJS.usuarios || objJS.usuario || null;
        if (!dados) {
            throw new ErrorResponse(400, "Dados inválidos", {
                message: "Objeto 'usuarios' é obrigatório",
            });
        }

        if (dados.nomeUsuario || dados.nome) {
            usuarioExistente.setNomeUsuario(dados.nomeUsuario || dados.nome);
        }
        if (dados.email) {
            usuarioExistente.setEmail(dados.email);
        }
        if (dados.senha && (dados.senha).trim() !== "") {
            const senhaPura = String(dados.senha);
            // Verifica se já é hash para evitar double-hash
            const isHashed = senhaPura.startsWith('$2a$') || senhaPura.startsWith('$2b$') || senhaPura.startsWith('$2y$');
            const senhaFinal = isHashed ? senhaPura : await bcrypt.hash(senhaPura, 10);
            usuarioExistente.setSenha(senhaFinal);
        }
        if (dados.tel) {
            usuarioExistente.setTel(dados.tel);
        }
        if (dados.tipoUsuario || dados.tipo_usuario) {
            usuarioExistente.setTipoUsuario(dados.tipoUsuario || dados.tipo_usuario);
        }
        if (dados.data_nasc || dados.dataNasc) {
            usuarioExistente.setDataNasc(dados.data_nasc || dados.dataNasc);
        }

        await this.usuariosDAO.update(usuarioExistente);
        return usuarioExistente;
    }

    async deleteService(idUsuario) {
        console.log("🟣 UsuariosService::deleteService()");

        const usuarioExistente = await this.usuariosDAO.findById(idUsuario);
        if (!usuarioExistente) {
            throw new ErrorResponse(404, "Usuário não encontrado", {
                message: `Não existe usuário com id ${idUsuario}`,
            });
        }

        return await this.usuariosDAO.delete(usuarioExistente);
    }
}

module.exports = UsuariosService;
