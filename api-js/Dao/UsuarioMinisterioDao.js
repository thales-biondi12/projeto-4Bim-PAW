const UsuarioMinisterio = require('../Models/UsuarioMinisterio');

class UsuarioMinisterioDao {
    constructor(db) {
        this.db = db;
    }

    async create(vinculo) {
        const sql = `
            INSERT INTO usuarios_ministerios (id_usuario, id_ministerio, data_entrada, funcao)
            VALUES (?, ?, ?, ?)
        `;
        const params = [
            vinculo.getIdUsuario(),
            vinculo.getIdMinisterio(),
            vinculo.getDataEntrada(),
            vinculo.getFuncao(),
        ];

        const conn = await this.db.getConnection();
        const [result] = await conn.execute(sql, params);

        vinculo.setId(result.insertId);
        return vinculo;
    }

    async findAll() {
        const sql = `
            SELECT um.*, u.nome as nome_usuario, mi.nome as nome_ministerio
            FROM usuarios_ministerios um
            LEFT JOIN usuarios u ON u.id_usuarios = um.id_usuario
            LEFT JOIN ministerios mi ON mi.id_ministerios = um.id_ministerio
            ORDER BY um.id_usuarios_ministerios DESC
        `;

        const conn = await this.db.getConnection();
        const [rows] = await conn.execute(sql);

        const listaVinculos = [];
        for (const row of rows) {
            const vinculo = new UsuarioMinisterio();
            vinculo.setId(parseInt(row.id_usuarios_ministerios));
            vinculo.setIdUsuario(parseInt(row.id_usuario));
            vinculo.setIdMinisterio(parseInt(row.id_ministerio));
            vinculo.setDataEntrada(row.data_entrada);
            vinculo.setFuncao(row.funcao);
            vinculo.setNomeUsuario(row.nome_usuario || null);
            vinculo.setNomeMinisterio(row.nome_ministerio || null);
            listaVinculos.push(vinculo);
        }
        return listaVinculos;
    }

    async findById(id) { return (await this.findAll()).find(v => v.getId() === Number(id)) || null; }
    async count() { const c=await this.db.getConnection(); const [r]=await c.execute('SELECT COUNT(*) qtd FROM usuarios_ministerios'); return Number(r[0]?.qtd||0); }
    async update(v) { const c=await this.db.getConnection(); const [r]=await c.execute('UPDATE usuarios_ministerios SET id_usuario=?,id_ministerio=?,data_entrada=?,funcao=? WHERE id_usuarios_ministerios=?',[v.getIdUsuario(),v.getIdMinisterio(),v.getDataEntrada(),v.getFuncao(),v.getId()]); return r.affectedRows>0; }

    async delete(id) {
        const sql = "DELETE FROM usuarios_ministerios WHERE id_usuarios_ministerios = ?";
        const conn = await this.db.getConnection();
        const [result] = await conn.execute(sql, [id]);
        return result.affectedRows > 0;
    }

    async exists(idUsuario, idMinisterio) {
        const sql = "SELECT 1 FROM usuarios_ministerios WHERE id_usuario = ? AND id_ministerio = ?";
        const conn = await this.db.getConnection();
        const [rows] = await conn.execute(sql, [idUsuario, idMinisterio]);
        return rows.length > 0;
    }
    async existsOther(u,m,id) { const c=await this.db.getConnection(); const [r]=await c.execute('SELECT 1 FROM usuarios_ministerios WHERE id_usuario=? AND id_ministerio=? AND id_usuarios_ministerios<>?',[u,m,id]); return r.length>0; }
}

module.exports = UsuarioMinisterioDao;
