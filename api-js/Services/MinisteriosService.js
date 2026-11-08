const Ministerios = require('../Models/Ministerios');
const MinisterioDao = require('../Dao/MinisterioDao');
const UsuariosDao = require('../Dao/UsuariosDao');
const ErrorResponse = require('../Http/ErrorResponse');

class MinisteriosService {
    constructor(ministerioDAODependency, usuariosDAODependency) {
        console.log("⬆️ MinisteriosService::__construct()");
        this.ministerioDAO = ministerioDAODependency;
        this.usuariosDAO = usuariosDAODependency;
    }

    async validateCoordinator(idCoordenador) {
        if (!(await this.usuariosDAO.findById(idCoordenador))) {
            throw new ErrorResponse(400, "Coordenador não encontrado", {
                message: `O usuário com id ${idCoordenador} não existe. Verifique o id do coordenador.`,
            });
        }
    }

    async createService(objJS) {
        console.log("🟣 MinisteriosService::createService()");

        const ministeriosData = objJS.ministerios || {};
        const idCoord = parseInt(ministeriosData.idCoordenador || ministeriosData.id_coordenador || 0);
        const dia = ministeriosData.diaReuniao || ministeriosData.dia_reuniao || null;

        await this.validateCoordinator(idCoord);

        const ministerio = new Ministerios();
        ministerio.setNome(ministeriosData.nome);
        ministerio.setDescricao(ministeriosData.descricao || null);
        ministerio.setDiaReuniao(dia);
        ministerio.setIdCoordenador(idCoord);

        const resultado = await this.ministerioDAO.findByField("nome", ministerio.getNome());
        if (resultado && resultado.length > 0) {
            throw new ErrorResponse(400, "Ministério já existe", {
                message: `O ministério ${ministerio.getNome()} já está cadastrado`,
            });
        }

        return await this.ministerioDAO.create(ministerio);
    }

    async countService() {
        console.log("🟣 MinisteriosService::countService()");
        return await this.ministerioDAO.count();
    }

    async findAllService() {
        console.log("🟣 MinisteriosService::findAllService()");
        return await this.ministerioDAO.findAll();
    }

    async findByIdService(idMinisterio) {
        console.log("🟣 MinisteriosService::findByIdService()");
        return await this.ministerioDAO.findById(idMinisterio);
    }

    async updateService(idMinisterio, objJS) {
        console.log("🟣 MinisteriosService::updateService()");

        const ministeriosData = objJS.ministerios || {};
        const idCoord = parseInt(ministeriosData.idCoordenador || ministeriosData.id_coordenador || 0);
        const dia = ministeriosData.diaReuniao || ministeriosData.dia_reuniao || null;

        await this.validateCoordinator(idCoord);

        const ministerioExistente = await this.ministerioDAO.findById(idMinisterio);
        if (!ministerioExistente) {
            throw new ErrorResponse(404, "Ministério não encontrado", {
                message: `Não existe ministério com id ${idMinisterio}`,
            });
        }

        ministerioExistente.setNome(ministeriosData.nome);
        ministerioExistente.setDescricao(ministeriosData.descricao || null);
        ministerioExistente.setDiaReuniao(dia);
        ministerioExistente.setIdCoordenador(idCoord);

        await this.ministerioDAO.update(ministerioExistente);
        return ministerioExistente;
    }

    async deleteService(idMinisterio) {
        console.log("🟣 MinisteriosService::deleteService()");

        const ministerioExistente = await this.ministerioDAO.findById(idMinisterio);
        if (!ministerioExistente) {
            throw new ErrorResponse(404, "Ministério não encontrado", {
                message: `Não existe ministério com id ${idMinisterio}`,
            });
        }

        return await this.ministerioDAO.delete(ministerioExistente);
    }
}

module.exports = MinisteriosService;
