const Mensagens = require('../Models/Mensagens');
const MensagemDao = require('../Dao/MensagemDao');
const UsuariosDao = require('../Dao/UsuariosDao');
const ErrorResponse = require('../Http/ErrorResponse');

class MensagensService {
    constructor(mensagemDAODependency, usuariosDAODependency) {
        console.log("⬆️ MensagensService::__construct()");
        this.mensagemDAO = mensagemDAODependency;
        this.usuariosDAO = usuariosDAODependency;
    }

    async createService(objJS) {
        console.log("🟣 MensagensService::createService()");

        const mensagensData = objJS.mensagens || {};
        const titulo = (mensagensData.titulo || "").trim();
        const conteudo = (mensagensData.conteudo || "").trim();
        const usuarioId = mensagensData.usuarioId || null;
        const dataPostagem = mensagensData.dataPostagem || null;

        if (titulo === "") {
            throw new ErrorResponse(400, "Título inválido", {
                message: "O título da mensagem não pode ser vazio.",
            });
        }

        if (conteudo === "") {
            throw new ErrorResponse(400, "Conteúdo inválido", {
                message: "O conteúdo da mensagem não pode ser vazio.",
            });
        }

        if (!usuarioId || !(await this.usuariosDAO.findById(usuarioId))) {
            throw new ErrorResponse(400, "Usuário não encontrado", {
                message: `O usuário com id ${usuarioId} não existe.`,
            });
        }

        const dateStr = dataPostagem || new Date().toISOString().split('T')[0];

        const mensagem = new Mensagens();
        mensagem.setTitulo(titulo);
        mensagem.setConteudo(conteudo);
        mensagem.setUsuarioId(usuarioId);
        mensagem.setDataPostagem(dateStr);

        return await this.mensagemDAO.create(mensagem);
    }

    async countService() {
        console.log("🟣 MensagensService::countService()");
        return await this.mensagemDAO.count();
    }

    async findAllService() {
        console.log("🟣 MensagensService::findAllService()");
        return await this.mensagemDAO.findAll();
    }

    async findByIdService(idMensagens) {
        console.log("🟣 MensagensService::findByIdService()");
        return await this.mensagemDAO.findById(idMensagens);
    }

    async updateService(idMensagens, objJS) {
        console.log("🟣 MensagensService::updateService()");

        const mensagemExistente = await this.mensagemDAO.findById(idMensagens);
        if (!mensagemExistente) {
            throw new ErrorResponse(404, "Mensagem não encontrada", {
                message: `Não existe mensagem com id ${idMensagens}`,
            });
        }

        const mensagensData = objJS.mensagens || {};
        const titulo = (mensagensData.titulo || "").trim();
        const conteudo = (mensagensData.conteudo || "").trim();
        const usuarioId = mensagensData.usuarioId || null;
        const dataPostagem = mensagensData.dataPostagem || null;

        if (titulo === "") {
            throw new ErrorResponse(400, "Título inválido", {
                message: "O título da mensagem não pode ser vazio.",
            });
        }

        if (conteudo === "") {
            throw new ErrorResponse(400, "Conteúdo inválido", {
                message: "O conteúdo da mensagem não pode ser vazio.",
            });
        }

        if (!usuarioId || !(await this.usuariosDAO.findById(usuarioId))) {
            throw new ErrorResponse(400, "Usuário não encontrado", {
                message: `O usuário com id ${usuarioId} não existe.`,
            });
        }

        mensagemExistente.setTitulo(titulo);
        mensagemExistente.setConteudo(conteudo);
        mensagemExistente.setUsuarioId(usuarioId);
        mensagemExistente.setDataPostagem(dataPostagem);

        await this.mensagemDAO.update(mensagemExistente);
        return mensagemExistente;
    }

    async deleteService(idMensagens) {
        console.log("🟣 MensagensService::deleteService()");

        const mensagemExistente = await this.mensagemDAO.findById(idMensagens);
        if (!mensagemExistente) {
            throw new ErrorResponse(404, "Mensagem não encontrada", {
                message: `Não existe mensagem com id ${idMensagens}`,
            });
        }

        return await this.mensagemDAO.delete(mensagemExistente);
    }
}

module.exports = MensagensService;
