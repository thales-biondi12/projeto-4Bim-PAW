const MinisteriosService = require('../Services/MinisteriosService');

class MinisteriosController {
    constructor(ministeriosServiceDependency) {
        console.log("⬆️ MinisteriosController::__construct()");
        this.ministeriosService = ministeriosServiceDependency;
    }

    async createController(req, res) {
        console.log("🔵 MinisteriosController::createController()");
        const objJS = req.body;
        const novoMinisterio = await this.ministeriosService.createService(objJS);

        return res.status(201).json({
            success: true,
            message: "Cadastro realizado com sucesso",
            data: {
                ministerios: [novoMinisterio.toJSON()]
            }
        });
    }

    async findAllController(req, res) {
        console.log("🔵 MinisteriosController::findAllController()");
        const ministerios = await this.ministeriosService.findAllService();

        return res.status(200).json({
            success: true,
            message: "Busca realizada com sucesso",
            data: {
                ministerios: ministerios.map(m => m.toJSON())
            }
        });
    }

    async findByIdController(req, res) {
        console.log("🔵 MinisteriosController::findByIdController()");
        const idMinisterio = parseInt(req.params.idMinisterios);
        const ministerio = await this.ministeriosService.findByIdService(idMinisterio);

        if (ministerio) {
            return res.status(200).json({
                success: true,
                message: "Busca realizada com sucesso",
                data: {
                    ministerios: [ministerio.toJSON()]
                }
            });
        } else {
            return res.status(404).json({
                success: false,
                message: "Ministério não encontrado"
            });
        }
    }

    async updateController(req, res) {
        console.log("🔵 MinisteriosController::updateController()");
        const idMinisterio = parseInt(req.params.idMinisterios);
        const objJS = req.body;
        const ministerioAtualizado = await this.ministeriosService.updateService(idMinisterio, objJS);

        return res.status(200).json({
            success: true,
            message: "Atualização realizada com sucesso",
            data: {
                ministerios: [ministerioAtualizado.toJSON()]
            }
        });
    }

    async deleteController(req, res) {
        console.log("🔵 MinisteriosController::deleteController()");
        const idMinisterio = parseInt(req.params.idMinisterios);
        const deletado = await this.ministeriosService.deleteService(idMinisterio);

        if (deletado) {
            return res.status(200).json({
                success: true,
                message: "Ministério deletado com sucesso"
            });
        } else {
            return res.status(404).json({
                success: false,
                message: "Ministério não encontrado"
            });
        }
    }

    async countController(req, res) {
        console.log("🔵 MinisteriosController::countController()");
        const total = await this.ministeriosService.countService();

        return res.status(200).json({
            success: true,
            message: "Executado com sucesso",
            data: {
                count: total
            }
        });
    }
}

module.exports = MinisteriosController;
