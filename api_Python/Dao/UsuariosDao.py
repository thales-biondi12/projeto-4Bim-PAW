import logging
from typing import List, Optional, Any
from ..Models.Usuarios import Usuarios
from ..Database.MysqlDatabase import MysqlDatabase

class UsuariosDao:
    """
    Classe responsável pelo acesso aos dados da entidade Usuários.
    """
    def __init__(self, database_instance: MysqlDatabase):
        self.database = database_instance
        logging.info("⬆️ UsuariosDao::__init__")

    def create(self, obj_usuarios: Usuarios) -> Usuarios:
        logging.info("🟢 UsuariosDao::create")
        sql = """
            INSERT INTO usuarios (nome, email, senha, tel, tipo_usuario, data_nasc)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            obj_usuarios.get_nome(),
            obj_usuarios.get_email(),
            obj_usuarios.get_senha(),
            obj_usuarios.get_tel(),
            obj_usuarios.get_tipo_usuario(),
            obj_usuarios.get_data_nasc()
        )

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        obj_usuarios.set_id_usuarios(cursor.lastrowid)
        return obj_usuarios

    def delete(self, obj_usuarios_model: Usuarios) -> bool:
        logging.info("🟢 UsuariosDao::delete")
        conn = self.database.get_connection()
        id_u = obj_usuarios_model.get_id_usuarios()

        try:
            # Em Python, para transações com mysql-connector, usamos conn.start_transaction()

            # Limpa referências (estranha a falta de CASCADE no banco)
            cursor = conn.cursor()

            cursor.execute("UPDATE ministerios SET id_coordenador = NULL WHERE id_coordenador = %s", (id_u,))
            cursor.execute("DELETE FROM inscricoes WHERE usuario_id = %s", (id_u,))
            cursor.execute("DELETE FROM mensagens WHERE usuario_id = %s", (id_u,))
            cursor.execute("DELETE FROM usuarios_ministerios WHERE id_usuario = %s", (id_u,))

            cursor.execute("DELETE FROM usuarios WHERE id_usuarios = %s", (id_u,))
            ok = cursor.rowcount > 0

            conn.commit()
            return ok
        except Exception as e:
            if hasattr(conn, "rollback"):
                conn.rollback()
            logging.error(f"Erro delete usuario: {e}")
            raise Exception(f"Erro ao excluir usuário: {e}")

    def update(self, obj_usuarios_model: Usuarios) -> bool:
        logging.info("🟢 UsuariosDao::update")
        sql = """
            UPDATE usuarios
            SET nome = %s, email = %s, senha = %s, tel = %s, tipo_usuario = %s, data_nasc = %s
            WHERE id_usuarios = %s
        """
        params = (
            obj_usuarios_model.get_nome(),
            obj_usuarios_model.get_email(),
            obj_usuarios_model.get_senha(),
            obj_usuarios_model.get_tel(),
            obj_usuarios_model.get_tipo_usuario(),
            obj_usuarios_model.get_data_nasc(),
            obj_usuarios_model.get_id_usuarios()
        )

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        return cursor.rowcount > 0

    def find_all(self) -> List[Usuarios]:
        logging.info("🟢 UsuariosDao::find_all")
        sql = "SELECT * FROM usuarios"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()

        usuarios = []
        for row in rows:
            usuario = Usuarios()
            usuario.set_id_usuarios(int(row["id_usuarios"]))
            usuario.set_nome_usuario(row["nome"])
            usuario.set_email(row["email"])
            usuario.set_senha(row["senha"])
            usuario.set_tel(row.get("tel"))
            usuario.set_tipo_usuario(row.get("tipo_usuario"))
            usuario.set_data_nasc(row.get("data_nasc"))
            usuarios.append(usuario)

        return usuarios

    def count(self) -> int:
        logging.info("🟢 UsuariosDao::count")
        sql = "SELECT COUNT(*) AS qtd FROM usuarios"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        row = cursor.fetchone()

        return int(row["qtd"]) if row else 0

    def find_by_id(self, id_usuarios: int) -> Optional[Usuarios]:
        logging.info("🟢 UsuariosDao::find_by_id")
        resultado = self.find_by_field("id_usuarios", id_usuarios)
        return resultado[0] if resultado else None

    def find_by_field(self, field: str, value: Any) -> List[Usuarios]:
        logging.info("🟢 UsuariosDao::find_by_field")
        campos_permitidos = ["id_usuarios", "nome", "email", "senha"]

        if field not in campos_permitidos:
            raise Exception("Campo inválido.")

        sql = f"SELECT * FROM usuarios WHERE {field} = %s"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (value,))
        rows = cursor.fetchall()

        usuarios = []
        for row in rows:
            usuario = Usuarios()
            usuario.set_id_usuarios(int(row["id_usuarios"]))
            usuario.set_nome_usuario(row["nome"])
            usuario.set_email(row["email"])
            usuario.set_senha(row["senha"])
            usuario.set_tel(row.get("tel"))
            usuario.set_tipo_usuario(row.get("tipo_usuario"))
            usuario.set_data_nasc(row.get("data_nasc"))
            usuarios.append(usuario)

        return usuarios
