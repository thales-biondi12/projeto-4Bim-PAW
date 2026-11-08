const UsuariosService = require('../Services/UsuariosService');
const MeuTokenJWT = require('../Http/MeuTokenJWT');

class UsuariosController {
    constructor(usuariosServiceDependency) {
        console.log("UsuariosController::__construct()");
        this.usuariosService = usuariosServiceDependency;
    }

    async createController(req, res) {
        console.log("UsuariosController::createController()");
        const objJS = req.body;
        const novoUsuario = await this.usuariosService.createService(objJS);

        return res.status(201).json({
            success: true,
            message: "Cadastro realizado com sucesso",
            data: {
                usuarios: [novoUsuario.toJSON()]
            }
        });
    }

    async loginController(req, res) {
        console.log("UsuariosController::loginController()");
        const objJS = req.body;
        const usuario = await this.usuariosService.loginService(objJS);

        const jwt = new MeuTokenJWT();
        const claims = {
            idUsuario: usuario.getIdUsuario(),
            nomeUsuario: usuario.getNomeUsuario(),
            email: usuario.getEmail(),
            tipoUsuario: usuario.getTipoUsuario(),
            // Legado
            idFuncionario: usuario.getIdUsuario(),
            name: usuario.getNomeUsuario(),
            role: usuario.getTipoUsuario()
        };

        const token = jwt.gerarToken(claims);
        const expiresIn = jwt.getDuration();

        return res.status(200).json({
            success: true,
            message: "Login realizado com sucesso",
            data: {
                token: token,
                token_type: "Bearer",
                expires_in: expiresIn,
                usuario: {
                    idUsuario: usuario.getIdUsuario(),
                    nomeUsuario: usuario.getNomeUsuario(),
                    email: usuario.getEmail(),
                    tipoUsuario: usuario.getTipoUsuario(),
                }
            }
        });
    }

    async findAllController(req, res) {
        console.log("UsuariosController::findAllController()");
        const usuarios = await this.usuariosService.findAllService();

        return res.status(200).json({
            success: true,
            message: "Busca realizada com sucesso",
            data: {
                usuarios: usuarios.map(u => u.toJSON())
            }
        });
    }

    async findByIdController(req, res) {
        console.log("UsuariosController::findByIdController()");
        const idUsuario = parseInt(req.params.idUsuario);
        const usuario = await this.usuariosService.findByIdService(idUsuario);

        if (!usuario) {
            return res.status(404).json({
                success: false,
                message: `Nao existe usuario com id ${idUsuario}`
            });
        }

        return res.status(200).json({
            success: true,
            message: "Busca realizada com sucesso",
            data: {
                usuarios: [usuario.toJSON()]
            }
        });
    }

    async updateController(req, res) {
        console.log("UsuariosController::updateController()");
        const idUsuario = parseInt(req.params.idUsuario);
        const objJS = req.body;
        const usuarioAtualizado = await this.usuariosService.updateService(idUsuario, objJS);

        return res.status(200).json({
            success: true,
            message: "Atualizacao realizada com sucesso",
            data: {
                usuarios: [usuarioAtualizado.toJSON()]
            }
        });
    }

    async deleteController(req, res) {
        console.log("UsuariosController::deleteController()");
        const idUsuario = parseInt(req.params.idUsuario);
        const deletado = await this.usuariosService.deleteService(idUsuario);

        return res.status(200).json({
            success: deletado,
            message: "Usuário excluído com sucesso"
        });
    }

    async countController(req, res) {
        console.log("UsuariosController::countController()");
        const total = await this.usuariosService.countService();

        return res.status(200).json({
            success: true,
            data: {
                count: total
            }
        });
    }
}

module.exports = UsuariosController;
