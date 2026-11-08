const MensagensService = require('../Services/MensagensService');

class MensagensController {
    constructor(mensagensServiceDependency) {
        console.log("⬆️ MensagensController::__construct()");
        this.mensagensService = mensagensServiceDependency;
    }

    async createController(req, res) {
        console.log("🔵 MensagensController::createController()");
        const objJS = req.body;

        if (req.user) {
            if (!objJS.mensagens?.usuarioId) {
                objJS.mensagens = objJS.mensagens || {};
                objJS.mensagens.usuarioId = req.user.idUsuario || req.user.idFuncionario;
            }
            if (!objJS.mensagens?.dataPostagem) {
                objJS.mensagens.dataPostagem = new Date().toISOString().split('T')[0];
            }
        }

        const novoMensagem = await this.mensagensService.createService(objJS);

        return res.status(201).json({
            success: true,
            message: "Cadastro realizado com sucesso",
            data: {
                mensagens: [novoMensagem.toJSON()]
            }
        });
    }

    async findAllController(req, res) {
        console.log("🔵 MensagensController::findAllController()");
        const mensagens = await this.mensagensService.findAllService();

        return res.status(200).json({
            success: true,
            message: "Busca realizada com sucesso",
            data: {
                mensagens: mensagens.map(m => m.toJSON())
            }
        });
    }

    async findByIdController(req, res) {
        const mensagem = await this.mensagensService.findByIdService(parseInt(req.params.idMensagens));
        if (!mensagem) return res.status(404).json({ success: false, message: 'Mensagem não encontrada' });
        return res.status(200).json({ success: true, message: 'Busca realizada com sucesso', data: { mensagens: [mensagem.toJSON()] } });
    }

    async updateController(req, res) {
        console.log("🔵 MensagensController::updateController()");
        const idMensagem = parseInt(req.params.idMensagens);
        const objJS = req.body;
        const mensagemAtualizada = await this.mensagensService.updateService(idMensagem, objJS);

        return res.status(200).json({
            success: true,
            message: "Atualização realizada com sucesso",
            data: {
                mensagens: [mensagemAtualizada.toJSON()]
            }
        });
    }

    async deleteController(req, res) {
        console.log("🔵 MensagensController::deleteController()");
        const idMensagem = parseInt(req.params.idMensagens);
        const deletado = await this.mensagensService.deleteService(idMensagem);

        if (deletado) {
            return res.status(200).json({
                success: true,
                message: "Mensagem deletada com sucesso"
            });
        } else {
            return res.status(404).json({
                success: false,
                message: "Mensagem não encontrada"
            });
        }
    }

    async countController(req, res) {
        console.log("🔵 MensagensController::countController()");
        const total = await this.mensagensService.countService();

        return res.status(200).json({
            success: true,
            message: "Executado com sucesso",
            data: {
                count: total
            }
        });
    }
}

module.exports = MensagensController;
