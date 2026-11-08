const InscricoesService = require('../Services/InscricoesService');

class InscricoesController {
    constructor(inscricoesServiceDependency) {
        console.log("⬆️ InscricoesController::__construct()");
        this.inscricoesService = inscricoesServiceDependency;
    }

    async createController(req, res) {
        console.log("🔵 InscricoesController::createController()");
        const objJS = req.body;

        // Injeta usuário logado se não enviado (simulando o jwtPayload do PHP)
        if (req.user && !objJS.inscricoes?.usuarioId) {
            objJS.inscricoes = objJS.inscricoes || {};
            objJS.inscricoes.usuarioId = req.user.idUsuario || req.user.idFuncionario;
        }

        const novoInscricao = await this.inscricoesService.createService(objJS);

        return res.status(201).json({
            success: true,
            message: "Cadastro realizado com sucesso",
            data: {
                inscricoes: [novoInscricao.toJSON()]
            }
        });
    }

    async findAllController(req, res) {
        console.log("🔵 InscricoesController::findAllController()");
        const inscricoes = await this.inscricoesService.findAllService();

        return res.status(200).json({
            success: true,
            message: "Busca realizada com sucesso",
            data: {
                inscricoes: inscricoes.map(i => i.toJSON())
            }
        });
    }

    async findByIdController(req, res) {
        const inscricao = await this.inscricoesService.findByIdService(parseInt(req.params.idInscricoes));
        if (!inscricao) return res.status(404).json({ success: false, message: 'Inscrição não encontrada' });
        return res.status(200).json({ success: true, message: 'Busca realizada com sucesso', data: { inscricoes: [inscricao.toJSON()] } });
    }

    async updateController(req, res) {
        console.log("🔵 InscricoesController::updateController()");
        const idInscricao = parseInt(req.params.idInscricoes);
        const objJS = req.body;
        const inscricaoAtualizada = await this.inscricoesService.updateService(idInscricao, objJS);

        return res.status(200).json({
            success: true,
            message: "Atualização realizada com sucesso",
            data: {
                inscricoes: [inscricaoAtualizada.toJSON()]
            }
        });
    }

    async deleteController(req, res) {
        console.log("🔵 InscricoesController::deleteController()");
        const idInscricao = parseInt(req.params.idInscricoes);
        const deletado = await this.inscricoesService.deleteService(idInscricao);

        if (deletado) {
            return res.status(200).json({
                success: true,
                message: "Inscrição deletada com sucesso"
            });
        } else {
            return res.status(404).json({
                success: false,
                message: "Inscrição não encontrada"
            });
        }
    }

    async countController(req, res) {
        console.log("🔵 InscricoesController::countController()");
        const total = await this.inscricoesService.countService();

        return res.status(200).json({
            success: true,
            message: "Executado com sucesso",
            data: {
                count: total
            }
        });
    }
}

module.exports = InscricoesController;
