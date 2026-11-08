import logging
from typing import List, Optional, Any
from ..Models.Inscricoes import Inscricoes
from ..Database.MysqlDatabase import MysqlDatabase

class InscricaoDao:
    """
    Classe responsável pelo acesso aos dados da entidade Inscrições.
    """
    def __init__(self, database_instance: MysqlDatabase):
        self.database = database_instance
        logging.info("⬆️ InscricaoDao::__init__")

    def create(self, obj_inscricao: Inscricoes) -> Inscricoes:
        logging.info("🟢 InscricaoDao::create")
        sql = """
            INSERT INTO inscricoes
            (usuario_id, evento_id, data_inscricao, presenca)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            obj_inscricao.get_usuario_id(),
            obj_inscricao.get_evento_id(),
            obj_inscricao.get_data_inscricao(),
            obj_inscricao.get_presenca()
        )

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        obj_inscricao.set_id_inscricoes(cursor.lastrowid)
        return obj_inscricao

    def delete(self, obj_inscricao_model: Inscricoes) -> bool:
        logging.info("🟢 InscricaoDao::delete")
        sql = "DELETE FROM inscricoes WHERE id_inscricoes = %s"
        params = (obj_inscricao_model.get_id_inscricoes(),)

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        return cursor.rowcount > 0

    def update(self, obj_inscricao_model: Inscricoes) -> bool:
        logging.info("🟢 InscricaoDao::update")
        sql = """
            UPDATE inscricoes
            SET usuario_id = %s, evento_id = %s, data_inscricao = %s, presenca = %s
            WHERE id_inscricoes = %s
        """
        params = (
            obj_inscricao_model.get_usuario_id(),
            obj_inscricao_model.get_evento_id(),
            obj_inscricao_model.get_data_inscricao(),
            obj_inscricao_model.get_presenca(),
            obj_inscricao_model.get_id_inscricoes()
        )

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        return cursor.rowcount > 0

    def find_all(self) -> List[Inscricoes]:
        logging.info("🟢 InscricaoDao::find_all")
        sql = """
            SELECT i.*, u.nome as nome_usuario, e.titulo as titulo_evento
            FROM inscricoes i
            LEFT JOIN usuarios u ON u.id_usuarios=i.usuario_id
            LEFT JOIN eventos e ON e.id_evento=i.evento_id
        """

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()

        inscricoes = []
        for row in rows:
            inscricao = Inscricoes()
            inscricao.set_id_inscricoes(int(row["id_inscricoes"]))
            inscricao.set_usuario_id(int(row["usuario_id"]))
            inscricao.set_evento_id(int(row["evento_id"]))
            inscricao.set_data_inscricao(row["data_inscricao"])
            inscricao.set_presenca(row["presenca"])
            inscricao.set_nome_usuario(row.get("nome_usuario"))
            inscricao.set_titulo_evento(row.get("titulo_evento"))
            inscricoes.append(inscricao)

        return inscricoes

    def count(self) -> int:
        logging.info("🟢 InscricaoDao::count")
        sql = "SELECT COUNT(*) AS qtd FROM inscricoes"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        row = cursor.fetchone()

        return int(row["qtd"]) if row else 0

    def find_by_id(self, id_inscricoes: int) -> Optional[Inscricoes]:
        logging.info("🟢 InscricaoDao::find_by_id")
        resultado = self.find_by_field("id_inscricoes", id_inscricoes)
        return resultado[0] if resultado else None

    def find_by_field(self, field: str, value: Any) -> List[Inscricoes]:
        logging.info("🟢 InscricaoDao::find_by_field")
        campos_permitidos = ["id_inscricoes", "usuario_id", "evento_id", "data_inscricao", "presenca"]

        if field not in campos_permitidos:
            raise Exception("Campo inválido.")

        sql = f"SELECT * FROM inscricoes WHERE {field} = %s"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (value,))
        rows = cursor.fetchall()

        inscricoes = []
        for row in rows:
            inscricao = Inscricoes()
            inscricao.set_id_inscricoes(int(row["id_inscricoes"]))
            inscricao.set_usuario_id(int(row["usuario_id"]))
            inscricao.set_evento_id(int(row["evento_id"]))
            inscricao.set_data_inscricao(row["data_inscricao"])
            inscricao.set_presenca(row["presenca"])
            inscricoes.append(inscricao)

        return inscricoes
