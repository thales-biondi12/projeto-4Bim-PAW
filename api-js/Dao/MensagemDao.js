const Mensagens = require('../Models/Mensagens');

class MensagemDao {
    constructor(databaseInstance) {
        this.database = databaseInstance;
        console.log("⬆️ MensagemDao::__construct()");
    }

    async create(objMensagem) {
        console.log("🟢 MensagemDao::create()");
        const sql = `
            INSERT INTO mensagens
            (titulo, conteudo, usuario_id, data_postagem)
            VALUES (?, ?, ?, ?)
        `;
        const params = [
            objMensagem.getTitulo(),
            objMensagem.getConteudo(),
            objMensagem.getUsuarioId(),
            objMensagem.getDataPostagem(),
        ];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        const novoID = result.insertId;
        objMensagem.setIdMensagens(novoID);

        return objMensagem;
    }

    async delete(objMensagemModel) {
        console.log("🟢 MensagemDao::delete()");
        const sql = "DELETE FROM mensagens WHERE id_mensagens = ?";
        const params = [objMensagemModel.getIdMensagens()];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        return result.affectedRows > 0;
    }

    async update(objMensagemModel) {
        console.log("🟢 MensagemDao::update()");
        const sql = `
            UPDATE mensagens
            SET titulo = ?, conteudo = ?, usuario_id = ?, data_postagem = ?
            WHERE id_mensagens = ?
        `;
        const params = [
            objMensagemModel.getTitulo(),
            objMensagemModel.getConteudo(),
            objMensagemModel.getUsuarioId(),
            objMensagemModel.getDataPostagem(),
            objMensagemModel.getIdMensagens(),
        ];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        return result.affectedRows > 0;
    }

    async findAll() {
        console.log("🟢 MensagemDao::findAll()");
        const sql = "SELECT * FROM mensagens";

        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql);

        const mensagens = [];
        for (const row of rows) {
            const mensagem = new Mensagens();
            mensagem.setIdMensagens(parseInt(row.id_mensagens));
            mensagem.setTitulo(row.titulo);
            mensagem.setConteudo(row.conteudo);
            mensagem.setUsuarioId(parseInt(row.usuario_id));
            mensagem.setDataPostagem(row.data_postagem);
            mensagens.push(mensagem);
        }
        return mensagens;
    }

    async count() {
        console.log("🟢 MensagemDao::count()");
        const sql = "SELECT COUNT(*) AS qtd FROM mensagens";

        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql);

        return parseInt(rows[0].qtd);
    }

    async findById(idMensagens) {
        console.log("🟢 MensagemDao::findById()");
        const resultado = await this.findByField("id_mensagens", idMensagens);
        if (resultado && resultado.length > 0) {
            return resultado[0];
        }
        return null;
    }

    async findByField(field, value) {
        console.log("🟢 MensagemDao::findByField()");
        const camposPermitidos = [
            "id_mensagens", "titulo", "conteudo", "usuario_id", "data_postagem",
        ];

        if (!camposPermitidos.includes(field)) {
            throw new Error("Campo inválido.");
        }

        const sql = `SELECT * FROM mensagens WHERE ${field} = ?`;
        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql, [value]);

        const mensagens = [];
        for (const row of rows) {
            const mensagem = new Mensagens();
            mensagem.setIdMensagens(parseInt(row.id_mensagens));
            mensagem.setTitulo(row.titulo);
            mensagem.setConteudo(row.conteudo);
            mensagem.setUsuarioId(parseInt(row.usuario_id));
            mensagem.setDataPostagem(row.data_postagem);
            mensagens.push(mensagem);
        }
        return mensagens;
    }
}

module.exports = MensagemDao;
