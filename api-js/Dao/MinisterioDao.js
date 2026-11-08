const Ministerios = require('../Models/Ministerios');

class MinisterioDao {
    constructor(databaseInstance) {
        this.database = databaseInstance;
        console.log("⬆️ MinisterioDao::__construct()");
    }

    async create(objMinisterios) {
        console.log("🟢 MinisterioDao::create()");
        const sql = `
            INSERT INTO ministerios (nome, descricao, dia_reuniao, id_coordenador)
            VALUES (?, ?, ?, ?)
        `;
        const params = [
            objMinisterios.getNome(),
            objMinisterios.getDescricao(),
            objMinisterios.getDiaReuniao(),
            objMinisterios.getIdCoordenador(),
        ];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        const novoID = result.insertId;
        objMinisterios.setIdMinisterios(novoID);
        return objMinisterios;
    }

    async delete(objMinisteriosModel) {
        console.log("🟢 MinisterioDao::delete()");
        const sql = "DELETE FROM ministerios WHERE id_ministerios = ?";
        const params = [objMinisteriosModel.getIdMinisterios()];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        return result.affectedRows > 0;
    }

    async update(objMinisteriosModel) {
        console.log("🟢 MinisterioDao::update()");
        const sql = `
            UPDATE ministerios
            SET nome = ?, descricao = ?, dia_reuniao = ?, id_coordenador = ?
            WHERE id_ministerios = ?
        `;
        const params = [
            objMinisteriosModel.getNome(),
            objMinisteriosModel.getDescricao(),
            objMinisteriosModel.getDiaReuniao(),
            objMinisteriosModel.getIdCoordenador(),
            objMinisteriosModel.getIdMinisterios(),
        ];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        return result.affectedRows > 0;
    }

    async findAll() {
        console.log("🟢 MinisterioDao::findAll()");
        const sql = `
            SELECT m.*, u.nome as nome_coordenador
            FROM ministerios m
            LEFT JOIN usuarios u ON u.id_usuarios = m.id_coordenador
        `;

        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql);

        const ministerios = [];
        for (const row of rows) {
            const ministerio = new Ministerios();
            ministerio.setIdMinisterios(parseInt(row.id_ministerios));
            ministerio.setNome(row.nome);
            ministerio.setDescricao(row.descricao || null);
            ministerio.setDiaReuniao(row.dia_reuniao);
            ministerio.setIdCoordenador(parseInt(row.id_coordenador));
            ministerio.setNomeCoordenador(row.nome_coordenador || null);
            ministerios.push(ministerio);
        }
        return ministerios;
    }

    async count() {
        console.log("🟢 MinisterioDao::count()");
        const sql = "SELECT COUNT(*) AS qtd FROM ministerios";

        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql);

        return parseInt(rows[0].qtd);
    }

    async findById(idMinisterios) {
        console.log("🟢 MinisterioDao::findById()");
        const resultado = await this.findByField("id_ministerios", idMinisterios);
        if (resultado && resultado.length > 0) {
            return resultado[0];
        }
        return null;
    }

    async findByField(field, value) {
        console.log("🟢 MinisterioDao::findByField()");
        const camposPermitidos = [
            "id_ministerios", "nome", "descricao", "dia_reuniao", "id_coordenador",
        ];

        if (!camposPermitidos.includes(field)) {
            throw new Error("Campo inválido.");
        }

        const sql = `SELECT * FROM ministerios WHERE ${field} = ?`;
        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql, [value]);

        const ministerios = [];
        for (const row of rows) {
            const ministerio = new Ministerios();
            ministerio.setIdMinisterios(parseInt(row.id_ministerios));
            ministerio.setNome(row.nome);
            ministerio.setDescricao(row.descricao || null);
            ministerio.setDiaReuniao(row.dia_reuniao);
            ministerio.setIdCoordenador(parseInt(row.id_coordenador));
            ministerios.push(ministerio);
        }
        return ministerios;
    }
}

module.exports = MinisterioDao;
