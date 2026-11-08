const Eventos = require('../Models/Eventos');

class EventosDao {
    constructor(databaseInstance) {
        this.database = databaseInstance;
        console.log("⬆️ EventosDao::__construct()");
    }

    async create(objEvento) {
        console.log("🟢 EventosDao::create()");
        const sql = `
            INSERT INTO eventos
            (titulo, descricao, data_evento, local_evento, limite_vagas, status_evento)
            VALUES (?, ?, ?, ?, ?, ?)
        `;
        const params = [
            objEvento.getTitulo(),
            objEvento.getDescricao(),
            objEvento.getDataEvento(),
            objEvento.getLocalEvento(),
            objEvento.getLimiteVagas(),
            objEvento.getStatusEvento(),
        ];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        const novoID = result.insertId;
        objEvento.setIdEvento(novoID);

        return objEvento;
    }

    async delete(objEventoModel) {
        console.log("🟢 EventosDao::delete()");
        const sql = "DELETE FROM eventos WHERE id_evento = ?";
        const params = [objEventoModel.getIdEvento()];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        return result.affectedRows > 0;
    }

    async update(objEventoModel) {
        console.log("🟢 EventosDao::update()");
        const sql = `
            UPDATE eventos
            SET titulo = ?, descricao = ?, data_evento = ?, local_evento = ?, limite_vagas = ?, status_evento = ?
            WHERE id_evento = ?
        `;
        const params = [
            objEventoModel.getTitulo(),
            objEventoModel.getDescricao(),
            objEventoModel.getDataEvento(),
            objEventoModel.getLocalEvento(),
            objEventoModel.getLimiteVagas(),
            objEventoModel.getStatusEvento(),
            objEventoModel.getIdEvento(),
        ];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        return result.affectedRows > 0;
    }

    async findAll() {
        console.log("🟢 EventosDao::findAll()");
        const sql = "SELECT * FROM eventos";

        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql);

        const eventos = [];
        for (const row of rows) {
            const evento = new Eventos();
            evento.setIdEvento(parseInt(row.id_evento));
            evento.setTitulo(row.titulo);
            evento.setDescricao(row.descricao);
            evento.setDataEvento(row.data_evento);
            evento.setLocalEvento(row.local_evento);
            evento.setLimiteVagas(parseInt(row.limite_vagas));
            evento.setStatusEvento(row.status_evento);
            eventos.push(evento);
        }
        return eventos;
    }

    async count() {
        console.log("🟢 EventosDao::count()");
        const sql = "SELECT COUNT(*) AS qtd FROM eventos";

        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql);

        return parseInt(rows[0].qtd);
    }

    async findById(idEvento) {
        console.log("🟢 EventosDao::findById()");
        const resultado = await this.findByField("id_evento", idEvento);
        if (resultado && resultado.length > 0) {
            return resultado[0];
        }
        return null;
    }

    async findByField(field, value) {
        console.log("🟢 EventosDao::findByField()");
        const camposPermitidos = [
            "id_evento", "titulo", "descricao", "data_evento", "local_evento", "limite_vagas", "status_evento",
        ];

        if (!camposPermitidos.includes(field)) {
            throw new Error("Campo inválido.");
        }

        const sql = `SELECT * FROM eventos WHERE ${field} = ?`;
        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql, [value]);

        const eventos = [];
        for (const row of rows) {
            const evento = new Eventos();
            evento.setIdEvento(parseInt(row.id_evento));
            evento.setTitulo(row.titulo);
            evento.setDescricao(row.descricao);
            evento.setDataEvento(row.data_evento);
            evento.setLocalEvento(row.local_evento);
            evento.setLimiteVagas(parseInt(row.limite_vagas));
            evento.setStatusEvento(row.status_evento);
            eventos.push(evento);
        }
        return eventos;
    }
}

module.exports = EventosDao;
