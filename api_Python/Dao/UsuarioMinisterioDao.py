import logging
from typing import List, Optional, Any
from ..Models.UsuarioMinisterio import UsuarioMinisterio
from ..Database.MysqlDatabase import MysqlDatabase

class UsuarioMinisterioDao:
    """
    Classe responsável pelo acesso aos dados da entidade vínculo Usuário-Ministério.
    """
    def __init__(self, db: MysqlDatabase):
        self.db = db

    def create(self, vinculo: UsuarioMinisterio) -> UsuarioMinisterio:
        logging.info("🟢 UsuarioMinisterioDao::create")
        sql = "INSERT INTO usuarios_ministerios (id_usuario, id_ministerio, data_entrada, funcao) VALUES (%s, %s, %s, %s)"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (
            vinculo.get_id_usuario(),
            vinculo.get_id_ministerio(),
            vinculo.get_data_entrada(),
            vinculo.get_funcao()
        ))
        conn.commit()

        vinculo.set_id(cursor.lastrowid)
        return vinculo

    def find_all(self) -> List[UsuarioMinisterio]:
        logging.info("🟢 UsuarioMinisterioDao::find_all")
        sql = """
            SELECT um.*, u.nome as nome_usuario, mi.nome as nome_ministerio
            FROM usuarios_ministerios um
            LEFT JOIN usuarios u ON u.id_usuarios=um.id_usuario
            LEFT JOIN ministerios mi ON mi.id_ministerios=um.id_ministerio
            ORDER BY um.id_usuarios_ministerios DESC
        """

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()

        lista_vinculos = []
        for row in rows:
            vinculo = UsuarioMinisterio()
            vinculo.set_id(int(row["id_usuarios_ministerios"]))
            vinculo.set_id_usuario(int(row["id_usuario"]))
            vinculo.set_id_ministerio(int(row["id_ministerio"]))
            vinculo.set_data_entrada(row["data_entrada"])
            vinculo.set_funcao(row["funcao"])
            vinculo.set_nome_usuario(row.get("nome_usuario"))
            vinculo.set_nome_ministerio(row.get("nome_ministerio"))
            lista_vinculos.append(vinculo)

        return lista_vinculos

    def delete(self, id_vinculo: int) -> bool:
        logging.info("🟢 UsuarioMinisterioDao::delete")
        sql = "DELETE FROM usuarios_ministerios WHERE id_usuarios_ministerios = %s"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id_vinculo,))
        conn.commit()

        return cursor.rowcount > 0

    def exists(self, id_usuario: int, id_ministerio: int) -> bool:
        logging.info("🟢 UsuarioMinisterioDao::exists")
        sql = "SELECT 1 FROM usuarios_ministerios WHERE id_usuario = %s AND id_ministerio = %s"

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id_usuario, id_ministerio))

        return cursor.fetchone() is not None
