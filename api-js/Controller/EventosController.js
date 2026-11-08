const EventosService = require('../Services/EventosService');

class EventosController {
    constructor(eventosServiceDependency) {
        console.log("⬆️ EventosController::__construct()");
        this.eventosService = eventosServiceDependency;
    }

    async createController(req, res) {
        console.log("🔵 EventosController::createController()");
        const objJS = req.body;
        const novoEvento = await this.eventosService.createService(objJS);

        return res.status(201).json({
            success: true,
            message: "Cadastro realizado com sucesso",
            data: {
                eventos: [novoEvento.toJSON()]
            }
        });
    }

    async findAllController(req, res) {
        console.log("🔵 EventosController::findAllController()");
        const eventos = await this.eventosService.findAllService();

        return res.status(200).json({
            success: true,
            message: "Busca realizada com sucesso",
            data: {
                eventos: eventos.map(e => e.toJSON())
            }
        });
    }

    async findByIdController(req, res) {
        const evento = await this.eventosService.findByIdService(parseInt(req.params.idEvento));
        if (!evento) return res.status(404).json({ success: false, message: 'Evento não encontrado' });
        return res.status(200).json({ success: true, message: 'Busca realizada com sucesso', data: { eventos: [evento.toJSON()] } });
    }

    async updateController(req, res) {
        console.log("🔵 EventosController::updateController()");
        const idEvento = parseInt(req.params.idEvento);
        const objJS = req.body;
        const eventoAtualizado = await this.eventosService.updateService(idEvento, objJS);

        return res.status(200).json({
            success: true,
            message: "Atualização realizada com sucesso",
            data: {
                eventos: [eventoAtualizado.toJSON()]
            }
        });
    }

    async deleteController(req, res) {
        console.log("🔵 EventosController::deleteController()");
        const idEvento = parseInt(req.params.idEvento);
        const deletado = await this.eventosService.deleteService(idEvento);

        if (deletado) {
            return res.status(200).json({
                success: true,
                message: "Evento deletado com sucesso"
            });
        } else {
            return res.status(404).json({
                success: false,
                message: "Evento não encontrado"
            });
        }
    }

    async countController(req, res) {
        console.log("🔵 EventosController::countController()");
        const total = await this.eventosService.countService();

        return res.status(200).json({
            success: true,
            message: "Executado com sucesso",
            data: {
                count: total
            }
        });
    }
}

module.exports = EventosController;
