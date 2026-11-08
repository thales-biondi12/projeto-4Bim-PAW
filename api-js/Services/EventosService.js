const Eventos = require('../Models/Eventos');
const ErrorResponse = require('../Http/ErrorResponse');

class EventosService {
    constructor(eventosDAODependency) {
        console.log("⬆️ EventosService::__construct()");
        this.eventosDAO = eventosDAODependency;
    }

    async createService(objJS) {
        console.log("🟣 EventosService::createService()");

        const eventosData = objJS.eventos || {};
        const titulo = (eventosData.titulo || "").trim();
        const descricao = eventosData.descricao || null;
        const dataEventoStr = eventosData.dataEvento || eventosData.data_evento || null;
        const localEvento = eventosData.localEvento || eventosData.local_evento || null;
        const limiteVagas = parseInt(eventosData.limiteVagas || eventosData.limite_vagas || 0);
        const statusEvento = eventosData.statusEvento || eventosData.status_evento || null;

        if (titulo === "") {
            throw new ErrorResponse(400, "Título inválido", {
                message: "O título do evento não pode ser vazio.",
            });
        }

        const existente = await this.eventosDAO.findByField("titulo", titulo);
        if (existente && existente.length > 0) {
            throw new ErrorResponse(400, "Evento já existe", {
                message: `O evento ${titulo} já está cadastrado`,
            });
        }

        if (!dataEventoStr) {
            throw new ErrorResponse(400, "Data inválida", {
                message: "A data do evento é obrigatória.",
            });
        }

        let dataEvento;
        try {
            dataEvento = new Date(dataEventoStr);
            if (isNaN(dataEvento.getTime())) throw new Error();
        } catch (e) {
            throw new ErrorResponse(400, "Data inválida", {
                message: "Formato de data inválido.",
            });
        }

        const hoje = new Date();
        hoje.setHours(0, 0, 0, 0);
        const dataEventoCompare = new Date(dataEvento);
        dataEventoCompare.setHours(0, 0, 0, 0);

        if (dataEventoCompare < hoje) {
            throw new ErrorResponse(400, "Data inválida", {
                message: "A data do evento não pode ser anterior à data atual.",
            });
        }

        if (limiteVagas < 0) {
            throw new ErrorResponse(400, "Limite inválido", {
                message: "O limite de vagas deve ser maior ou igual a zero.",
            });
        }

        const evento = new Eventos();
        evento.setTitulo(titulo);
        evento.setDescricao(descricao);
        evento.setDataEvento(dataEvento.toISOString().split('T')[0]);
        evento.setLocalEvento(localEvento);
        evento.setLimiteVagas(limiteVagas);
        evento.setStatusEvento(statusEvento);

        return await this.eventosDAO.create(evento);
    }

    async countService() {
        console.log("🟣 EventosService::countService()");
        return await this.eventosDAO.count();
    }

    async findAllService() {
        console.log("🟣 EventosService::findAllService()");
        return await this.eventosDAO.findAll();
    }

    async findByIdService(idEvento) {
        console.log("🟣 EventosService::findByIdService()");
        return await this.eventosDAO.findById(idEvento);
    }

    async updateService(idEvento, objJS) {
        console.log("🟣 EventosService::updateService()");

        const eventoExistente = await this.eventosDAO.findById(idEvento);
        if (!eventoExistente) {
            throw new ErrorResponse(404, "Evento não encontrado", {
                message: `Não existe evento com id ${idEvento}`,
            });
        }

        const eventosData = objJS.eventos || {};
        const titulo = (eventosData.titulo || "").trim();
        const descricao = eventosData.descricao || null;
        const dataEventoStr = eventosData.dataEvento || eventosData.data_evento || null;
        const localEvento = eventosData.localEvento || eventosData.local_evento || null;
        const limiteVagas = parseInt(eventosData.limiteVagas || eventosData.limite_vagas || 0);
        const statusEvento = eventosData.statusEvento || eventosData.status_evento || null;

        if (titulo === "") {
            throw new ErrorResponse(400, "Título inválido", {
                message: "O título do evento não pode ser vazio.",
            });
        }

        const existente = await this.eventosDAO.findByField("titulo", titulo);
        for (const eventoMesmoTitulo of existente) {
            if (eventoMesmoTitulo.getIdEvento() !== idEvento) {
                throw new ErrorResponse(400, "Evento já existe", {
                    message: `O evento ${titulo} já está cadastrado`,
                });
            }
        }

        if (!dataEventoStr) {
            throw new ErrorResponse(400, "Data inválida", {
                message: "A data do evento é obrigatória.",
            });
        }

        let dataEvento;
        try {
            dataEvento = new Date(dataEventoStr);
            if (isNaN(dataEvento.getTime())) throw new Error();
        } catch (e) {
            throw new ErrorResponse(400, "Data inválida", {
                message: "Formato de data inválido.",
            });
        }

        const hoje = new Date();
        hoje.setHours(0, 0, 0, 0);
        const dataEventoCompare = new Date(dataEvento);
        dataEventoCompare.setHours(0, 0, 0, 0);

        if (dataEventoCompare < hoje) {
            throw new ErrorResponse(400, "Data inválida", {
                message: "A data do evento não pode ser anterior à data atual.",
            });
        }

        if (limiteVagas < 0) {
            throw new ErrorResponse(400, "Limite inválido", {
                message: "O limite de vagas deve ser maior ou igual a zero.",
            });
        }

        eventoExistente.setTitulo(titulo);
        eventoExistente.setDescricao(descricao);
        eventoExistente.setDataEvento(dataEvento.toISOString().split('T')[0]);
        eventoExistente.setLocalEvento(localEvento);
        eventoExistente.setLimiteVagas(limiteVagas);
        eventoExistente.setStatusEvento(statusEvento);

        await this.eventosDAO.update(eventoExistente);
        return eventoExistente;
    }

    async deleteService(idEvento) {
        console.log("🟣 EventosService::deleteService()");

        const eventoExistente = await this.eventosDAO.findById(idEvento);
        if (!eventoExistente) {
            throw new ErrorResponse(404, "Evento não encontrado", {
                message: `Não existe evento com id ${idEvento}`,
            });
        }

        return await this.eventosDAO.delete(eventoExistente);
    }
}

module.exports = EventosService;
