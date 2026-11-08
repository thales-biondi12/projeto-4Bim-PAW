import logging
from typing import List, Optional, Any
from ..Models.Ministerios import Ministerios
from ..Database.MysqlDatabase import MysqlDatabase

class MinisterioDao:
    """
    Classe responsável pelo acesso aos dados da entidade Ministérios.
    """
    def __init__(self, database_instance: MysqlDatabase):
        self.database = database_instance
        logging.info("⬆️ MinisterioDao::__init__")

    def create(self, obj_ministerios: Ministerios) -> Ministerios:
        logging.info("🟢 MinisterioDao::create")
        sql = """
            INSERT INTO ministerios (nome, descricao, dia_reuniao, id_coordenador)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            obj_ministerios.get_nome(),
            obj_ministerios.get_descricao(),
            obj_ministerios.get_dia_reuniao(),
            obj_ministerios.get_id_coordenador()
        )

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        obj_ministerios.set_id_ministerios(cursor.lastrowid)
        return obj_ministerios

    def delete(self, obj_ministerios_model: Ministerios) -> bool:
        logging.info("🟢 MinisterioDao::delete")
        sql = "DELETE FROM ministerios WHERE id_ministerios = %s"
        params = (obj_ministerios_model.get_id_ministerios(),)

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        return cursor.rowcount > 0

    def update(self, obj_ministerios_model: Ministerios) -> bool:
        logging.info("🟢 MinisterioDao::update")
        sql = """
            UPDATE ministerios
            SET nome = %s, descricao = %s, dia_reuniao = %s, id_coordenador = %s
            WHERE id_ministerios = %s
        """
        params = (
            obj_ministerios_model.get_nome(),
            obj_ministerios_model.get_descricao(),
            obj_ministerios_model.get_dia_reuniao(),
            obj_ministerios_model.get_id_coordenador(),
            obj_ministerios_model.get_id_ministerios()
        )

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        return cursor.rowcount > 0

    def find_all(self) -> List[Ministerios]:
        logging.info("🟢 MinisterioDao::find_all")
        sql = """
            SELECT m.*, u.nome as nome_coordenador
            FROM ministerios m
            LEFT JOIN usuarios u ON u.id_usuarios = m.id_coordenador
        """

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()

        ministerios = []
        for row in rows:
            ministerio = Ministerios()
            ministerio.set_id_ministerios(int(row["id_ministerios"]))
            ministerio.set_nome(row["nome"])
            ministerio.set_descricao(row.get("descricao"))
            ministerio.set_dia_reuniao(row["dia_reuniao"])
            ministerio.set_id_coordenador(int(row["id_coordenador"]))
            ministerio.set_nome_coordenador(row.get("nome_coordenador"))
            ministerios.append(ministerio)

        return ministerios

    def count(self) -> int:
        logging.info("🟢 MinisterioDao::count")
        sql = "SELECT COUNT(*) AS qtd FROM ministerios"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        row = cursor.fetchone()

        return int(row["qtd"]) if row else 0

    def find_by_id(self, id_ministerios: int) -> Optional[Ministerios]:
        logging.info("🟢 MinisterioDao::find_by_id")
        resultado = self.find_by_field("id_ministerios", id_ministerios)
        return resultado[0] if resultado else None

    def find_by_field(self, field: str, value: Any) -> List[Ministerios]:
        logging.info("🟢 MinisterioDao::find_by_field")
        campos_permitidos = ["id_ministerios", "nome", "descricao", "dia_reuniao", "id_coordenador"]

        if field not in campos_permitidos:
            raise Exception("Campo inválido.")

        sql = f"SELECT * FROM ministerios WHERE {field} = %s"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (value,))
        rows = cursor.fetchall()

        ministerios = []
        for row in rows:
            ministerio = Ministerios()
            ministerio.set_id_ministerios(int(row["id_ministerios"]))
            ministerio.set_nome(row["nome"])
            ministerio.set_descricao(row.get("descricao"))
            ministerio.set_dia_reuniao(row["dia_reuniao"])
            ministerio.set_id_coordenador(int(row["id_coordenador"]))
            ministerios.append(ministerio)

        return ministerios
