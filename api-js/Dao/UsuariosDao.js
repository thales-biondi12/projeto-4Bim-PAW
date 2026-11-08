const Usuarios = require('../Models/Usuarios');

class UsuariosDao {
    constructor(databaseInstance) {
        this.database = databaseInstance;
        console.log("⬆️ UsuariosDAO::__construct()");
    }

    async create(objUsuarios) {
        console.log("🟢 UsuariosDAO::create()");
        const sql = `
            INSERT INTO usuarios (nome, email, senha, tel, tipo_usuario, data_nasc)
            VALUES (?, ?, ?, ?, ?, ?)
        `;
        const params = [
            objUsuarios.getNome(),
            objUsuarios.getEmail(),
            objUsuarios.getSenha(),
            objUsuarios.getTel(),
            objUsuarios.getTipoUsuario(),
            objUsuarios.getDataNasc(),
        ];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        const novoID = result.insertId;
        objUsuarios.setIdUsuarios(novoID);
        return objUsuarios;
    }

    async delete(objUsuariosModel) {
        console.log("🟢 UsuariosDAO::delete()");
        const pool = await this.database.getConnection();
        const conn = await pool.getConnection();
        const id = objUsuariosModel.getIdUsuarios();

        try {
            // Início de transação para garantir a exclusão de todas as referências
            await conn.beginTransaction();

            // 1. Limpa coordenação de ministérios
            await conn.execute("UPDATE ministerios SET id_coordenador = NULL WHERE id_coordenador = ?", [id]);

            // 2. Remove inscrições
            await conn.execute("DELETE FROM inscricoes WHERE usuario_id = ?", [id]);

            // 3. Remove mensagens
            await conn.execute("DELETE FROM mensagens WHERE usuario_id = ?", [id]);

            // 4. Remove vínculos com ministérios
            await conn.execute("DELETE FROM usuarios_ministerios WHERE id_usuario = ?", [id]);

            // 5. Remove o usuário
            const [result] = await conn.execute("DELETE FROM usuarios WHERE id_usuarios = ?", [id]);

            await conn.commit();
            return result.affectedRows > 0;
        } catch (e) {
            await conn.rollback().catch(() => {});
            console.error("Erro delete usuario: " + e.message);
            throw new Error("Erro ao excluir usuário: " + e.message);
        } finally {
            conn.release();
        }
    }

    async update(objUsuariosModel) {
        console.log("🟢 UsuariosDAO::update()");
        const sql = `
            UPDATE usuarios
            SET nome = ?, email = ?, senha = ?, tel = ?, tipo_usuario = ?, data_nasc = ?
            WHERE id_usuarios = ?
        `;
        const params = [
            objUsuariosModel.getNome(),
            objUsuariosModel.getEmail(),
            objUsuariosModel.getSenha(),
            objUsuariosModel.getTel(),
            objUsuariosModel.getTipoUsuario(),
            objUsuariosModel.getDataNasc(),
            objUsuariosModel.getIdUsuarios(),
        ];

        const conn = await this.database.getConnection();
        const [result] = await conn.execute(sql, params);

        return result.affectedRows > 0;
    }

    async findAll() {
        console.log("🟢 UsuariosDAO::findAll()");
        const sql = "SELECT * FROM usuarios";

        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql);

        const usuarios = [];
        for (const row of rows) {
            const usuario = new Usuarios();
            usuario.setIdUsuarios(parseInt(row.id_usuarios));
            usuario.setNomeUsuario(row.nome);
            usuario.setEmail(row.email);
            usuario.setSenha(row.senha);
            usuario.setTel(row.tel || null);
            usuario.setTipoUsuario(row.tipo_usuario || null);
            usuario.setDataNasc(row.data_nasc || null);
            usuarios.push(usuario);
        }
        return usuarios;
    }

    async count() {
        console.log("🟢 UsuariosDAO::count()");
        const sql = "SELECT COUNT(*) AS qtd FROM usuarios";

        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql);

        return parseInt(rows[0].qtd);
    }

    async findById(idUsuarios) {
        console.log("🟢 UsuariosDAO::findById()");
        const resultado = await this.findByField("id_usuarios", idUsuarios);
        if (resultado && resultado.length > 0) {
            return resultado[0];
        }
        return null;
    }

    async findByField(field, value) {
        console.log("🟢 UsuariosDAO::findByField()");
        const camposPermitidos = ["id_usuarios", "nome", "email", "senha"];

        if (!camposPermitidos.includes(field)) {
            throw new Error("Campo inválido.");
        }

        const sql = `SELECT * FROM usuarios WHERE ${field} = ?`;
        const conn = await this.database.getConnection();
        const [rows] = await conn.execute(sql, [value]);

        const usuarios = [];
        for (const row of rows) {
            const usuario = new Usuarios();
            usuario.setIdUsuarios(parseInt(row.id_usuarios));
            usuario.setNomeUsuario(row.nome);
            usuario.setEmail(row.email);
            usuario.setSenha(row.senha);
            usuario.setTel(row.tel || null);
            usuario.setTipoUsuario(row.tipo_usuario || null);
            usuario.setDataNasc(row.data_nasc || null);
            usuarios.push(usuario);
        }
        return usuarios;
    }
}

module.exports = UsuariosDao;
