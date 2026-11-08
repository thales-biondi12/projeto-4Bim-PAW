const Inscricoes = require('../Models/Inscricoes');
const InscricaoDao = require('../Dao/InscricaoDao');
const UsuariosDao = require('../Dao/UsuariosDao');
const EventosDao = require('../Dao/EventosDao');
const ErrorResponse = require('../Http/ErrorResponse');

class InscricoesService {
    constructor(inscricaoDAODependency, usuariosDAODependency, eventosDAODependency) {
        console.log("⬆️ InscricoesService::__construct()");
        this.inscricaoDAO = inscricaoDAODependency;
        this.usuariosDAO = usuariosDAODependency;
        this.eventosDAO = eventosDAODependency;
    }

    async createService(objJS) {
        console.log("🟣 InscricoesService::createService()");

        const inscricoesData = objJS.inscricoes || {};
        const usuarioId = inscricoesData.usuarioId || null;
        const eventoId = inscricoesData.eventoId || null;
        const dataInscricao = inscricoesData.dataInscricao || null;
        const presenca = inscricoesData.presenca || null;

        if (!usuarioId || !(await this.usuariosDAO.findById(usuarioId))) {
            throw new ErrorResponse(400, "Usuário não encontrado", {
                message: `O usuário com id ${usuarioId} não existe.`,
            });
        }

        if (!eventoId || !(await this.eventosDAO.findById(eventoId))) {
            throw new ErrorResponse(400, "Evento não encontrado", {
                message: `O evento com id ${eventoId} não existe.`,
            });
        }

        const inscricoesUsuario = await this.inscricaoDAO.findByField("usuario_id", usuarioId);
        for (const insc of inscricoesUsuario) {
            if (insc.getEventoId() === eventoId) {
                throw new ErrorResponse(400, "Inscrição duplicada", {
                    message: "Usuário já inscrito neste evento.",
                });
            }
        }

        const eventosInscricoes = await this.inscricaoDAO.findByField("evento_id", eventoId);
        const evento = await this.eventosDAO.findById(eventoId);
        if (evento && evento.getLimiteVagas() > 0 && eventosInscricoes.length >= evento.getLimiteVagas()) {
            throw new ErrorResponse(400, "Evento sem vagas", {
                message: "Não há vagas disponíveis neste evento.",
            });
        }

        const dateStr = dataInscricao || new Date().toISOString().split('T')[0];

        const inscricao = new Inscricoes();
        inscricao.setUsuarioId(usuarioId);
        inscricao.setEventoId(eventoId);
        inscricao.setDataInscricao(dateStr);
        inscricao.setPresenca(presenca);

        return await this.inscricaoDAO.create(inscricao);
    }

    async countService() {
        console.log("🟣 InscricoesService::countService()");
        return await this.inscricaoDAO.count();
    }

    async findAllService() {
        console.log("🟣 InscricoesService::findAllService()");
        return await this.inscricaoDAO.findAll();
    }

    async findByIdService(idInscricoes) {
        console.log("🟣 InscricoesService::findByIdService()");
        return await this.inscricaoDAO.findById(idInscricoes);
    }

    async updateService(idInscricoes, objJS) {
        console.log("🟣 InscricoesService::updateService()");

        const inscricaoExistente = await this.inscricaoDAO.findById(idInscricoes);
        if (!inscricaoExistente) {
            throw new ErrorResponse(404, "Inscricao não encontrada", {
                message: `Não existe inscrição com id ${idInscricoes}`,
            });
        }

        const inscricoesData = objJS.inscricoes || {};
        const usuarioId = inscricoesData.usuarioId || null;
        const eventoId = inscricoesData.eventoId || null;
        const dataInscricao = inscricoesData.dataInscricao || null;
        const presenca = inscricoesData.presenca || null;

        if (!usuarioId || !(await this.usuariosDAO.findById(usuarioId))) {
            throw new ErrorResponse(400, "Usuário não encontrado", {
                message: `O usuário com id ${usuarioId} não existe.`,
            });
        }

        if (!eventoId || !(await this.eventosDAO.findById(eventoId))) {
            throw new ErrorResponse(400, "Evento não encontrado", {
                message: `O evento com id ${eventoId} não existe.`,
            });
        }

        const inscricoesUsuario = await this.inscricaoDAO.findByField("usuario_id", usuarioId);
        for (const insc of inscricoesUsuario) {
            if (insc.getEventoId() === eventoId && insc.getIdInscricoes() !== idInscricoes) {
                throw new ErrorResponse(400, "Inscrição duplicada", {
                    message: "Usuário já inscrito neste evento.",
                });
            }
        }

        const evento = await this.eventosDAO.findById(eventoId);
        const eventosInscricoes = await this.inscricaoDAO.findByField("evento_id", eventoId);
        if (evento && evento.getLimiteVagas() > 0 &&
            inscricaoExistente.getEventoId() !== eventoId &&
            eventosInscricoes.length >= evento.getLimiteVagas()) {
            throw new ErrorResponse(400, "Evento sem vagas", {
                message: "Não há vagas disponíveis neste evento.",
            });
        }

        const dateStr = dataInscricao || new Date().toISOString().split('T')[0];

        inscricaoExistente.setUsuarioId(usuarioId);
        inscricaoExistente.setEventoId(eventoId);
        inscricaoExistente.setDataInscricao(dateStr);
        inscricaoExistente.setPresenca(presenca);

        await this.inscricaoDAO.update(inscricaoExistente);
        return inscricaoExistente;
    }

    async deleteService(idInscricoes) {
        console.log("🟣 InscricoesService::deleteService()");

        const inscricaoExistente = await this.inscricaoDAO.findById(idInscricoes);
        if (!inscricaoExistente) {
            throw new ErrorResponse(404, "Inscricao não encontrada", {
                message: `Não existe inscrição com id ${idInscricoes}`,
            });
        }

        return await this.inscricaoDAO.delete(inscricaoExistente);
    }
}

module.exports = InscricoesService;
