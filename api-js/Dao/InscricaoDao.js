const Inscricoes = require('../Models/Inscricoes');

class InscricaoDao {
    constructor(databaseInstance) {
        this.database = databaseInstance;
        console.log("⬆️ InscricaoDao::__construct()");
    }

    async create(objInscricao) {
        console.log("🟢 InscricaoDao::create()");
        const sql = `
            INSERT INTO inscricoes
            (usuario_id, evento_id, data_inscricao, presenca)
            VALUES (?, ?, ?, ?)
        `;
        const params = [
            objInscricao.getUsuarioId(),
            objInscricao.getEventoId(),
            objInscricao.getDataInscricao(),
            objInscricao.getPresenca(),
        ];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        const novoID = result.insertId;
        objInscricao.setIdInscricoes(novoID);

        return objInscricao;
    }

    async delete(objInscricaoModel) {
        console.log("🟢 InscricaoDao::delete()");
        const sql = "DELETE FROM inscricoes WHERE id_inscricoes = ?";
        const params = [objInscricaoModel.getIdInscricoes()];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        return result.affectedRows > 0;
    }

    async update(objInscricaoModel) {
        console.log("🟢 InscricaoDao::update()");
        const sql = `
            UPDATE inscricoes
            SET usuario_id = ?, evento_id = ?, data_inscricao = ?, presenca = ?
            WHERE id_inscricoes = ?
        `;
        const params = [
            objInscricaoModel.getUsuarioId(),
            objInscricaoModel.getEventoId(),
            objInscricaoModel.getDataInscricao(),
            objInscricaoModel.getPresenca(),
            objInscricaoModel.getIdInscricoes(),
        ];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        return result.affectedRows > 0;
    }

    async findAll() {
        console.log("🟢 InscricaoDao::findAll()");
        const sql = `
            SELECT i.*, u.nome as nome_usuario, e.titulo as titulo_evento
            FROM inscricoes i
            LEFT JOIN usuarios u ON u.id_usuarios = i.usuario_id
            LEFT JOIN eventos e ON e.id_evento = i.evento_id
        `;

        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql);

        const inscricoes = [];
        for (const row of rows) {
            const inscricao = new Inscricoes();
            inscricao.setIdInscricoes(parseInt(row.id_inscricoes));
            inscricao.setUsuarioId(parseInt(row.usuario_id));
            inscricao.setEventoId(parseInt(row.evento_id));
            inscricao.setDataInscricao(row.data_inscricao);
            inscricao.setPresenca(row.presenca);
            inscricao.setNomeUsuario(row.nome_usuario || null);
            inscricao.setTituloEvento(row.titulo_evento || null);
            inscricoes.push(inscricao);
        }
        return inscricoes;
    }

    async count() {
        console.log("🟢 InscricaoDao::count()");
        const sql = "SELECT COUNT(*) AS qtd FROM inscricoes";

        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql);

        return parseInt(rows[0].qtd);
    }

    async findById(idInscricoes) {
        console.log("🟢 InscricaoDao::findById()");
        const resultado = await this.findByField("id_inscricoes", idInscricoes);
        if (resultado && resultado.length > 0) {
            return resultado[0];
        }
        return null;
    }

    async findByField(field, value) {
        console.log("🟢 InscricaoDao::findByField()");
        const camposPermitidos = [
            "id_inscricoes", "usuario_id", "evento_id", "data_inscricao", "presenca",
        ];

        if (!camposPermitidos.includes(field)) {
            throw new Error("Campo inválido.");
        }

        const sql = `SELECT * FROM inscricoes WHERE ${field} = ?`;
        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql, [value]);

        const inscricoes = [];
        for (const row of rows) {
            const inscricao = new Inscricoes();
            inscricao.setIdInscricoes(parseInt(row.id_inscricoes));
            inscricao.setUsuarioId(parseInt(row.usuario_id));
            inscricao.setEventoId(parseInt(row.evento_id));
            inscricao.setDataInscricao(row.data_inscricao);
            inscricao.setPresenca(row.presenca);
            inscricoes.push(inscricao);
        }
        return inscricoes;
    }
}

module.exports = InscricaoDao;
