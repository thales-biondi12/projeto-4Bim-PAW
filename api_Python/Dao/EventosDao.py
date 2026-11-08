import logging
from typing import List, Optional, Any
from ..Models.Eventos import Eventos
from ..Database.MysqlDatabase import MysqlDatabase

class EventosDao:
    """
    Classe responsável pelo acesso aos dados da entidade Eventos.
    """
    def __init__(self, database_instance: MysqlDatabase):
        self.database = database_instance
        logging.info("⬆️ EventosDao::__init__")

    def create(self, obj_evento: Eventos) -> Eventos:
        logging.info("🟢 EventosDao::create")

        sql = """
            INSERT INTO eventos
            (titulo, descricao, data_evento, local_evento, limite_vagas, status_evento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            obj_evento.get_titulo(),
            obj_evento.get_descricao(),
            obj_evento.get_data_evento(),
            obj_evento.get_local_evento(),
            obj_evento.get_limite_vagas(),
            obj_evento.get_status_evento()
        )

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        obj_evento.set_id_evento(cursor.lastrowid)
        return obj_evento

    def delete(self, obj_evento_model: Eventos) -> bool:
        logging.info("🟢 EventosDao::delete")
        sql = "DELETE FROM eventos WHERE id_evento = %s"
        params = (obj_evento_model.get_id_evento(),)

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        return cursor.rowcount > 0

    def update(self, obj_evento_model: Eventos) -> bool:
        logging.info("🟢 EventosDao::update")
        sql = """
            UPDATE eventos
            SET titulo = %s, descricao = %s, data_evento = %s,
                local_evento = %s, limite_vagas = %s, status_evento = %s
            WHERE id_evento = %s
        """
        params = (
            obj_evento_model.get_titulo(),
            obj_evento_model.get_descricao(),
            obj_evento_model.get_data_evento(),
            obj_evento_model.get_local_evento(),
            obj_evento_model.get_limite_vagas(),
            obj_evento_model.get_status_evento(),
            obj_evento_model.get_id_evento()
        )

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        return cursor.rowcount > 0

    def find_all(self) -> List[Eventos]:
        logging.info("🟢 EventosDao::find_all")
        sql = "SELECT * FROM eventos"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()

        eventos = []
        for row in rows:
            evento = Eventos()
            evento.set_id_evento(int(row["id_evento"]))
            evento.set_titulo(row["titulo"])
            evento.set_descricao(row["descricao"])
            evento.set_data_evento(row["data_evento"])
            evento.set_local_evento(row["local_evento"])
            evento.set_limite_vagas(int(row["limite_vagas"]))
            evento.set_status_evento(row["status_evento"])
            eventos.append(evento)

        return eventos

    def count(self) -> int:
        logging.info("🟢 EventosDao::count")
        sql = "SELECT COUNT(*) AS qtd FROM eventos"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        row = cursor.fetchone()

        return int(row["qtd"]) if row else 0

    def find_by_id(self, id_evento: int) -> Optional[Eventos]:
        logging.info("🟢 EventosDao::find_by_id")
        resultado = self.find_by_field("id_evento", id_evento)
        return resultado[0] if resultado else None

    def find_by_field(self, field: str, value: Any) -> List[Eventos]:
        logging.info("🟢 EventosDao::find_by_field")
        campos_permitidos = [
            "id_evento", "titulo", "descricao", "data_evento",
            "local_evento", "limite_vagas", "status_evento"
        ]

        if field not in campos_permitidos:
            raise Exception("Campo inválido.")

        sql = f"SELECT * FROM eventos WHERE {field} = %s"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (value,))
        rows = cursor.fetchall()

        eventos = []
        for row in rows:
            evento = Eventos()
            evento.set_id_evento(int(row["id_evento"]))
            evento.set_titulo(row["titulo"])
            evento.set_descricao(row["descricao"])
            evento.set_data_evento(row["data_evento"])
            evento.set_local_evento(row["local_evento"])
            evento.set_limite_vagas(int(row["limite_vagas"]))
            evento.set_status_evento(row["status_evento"])
            eventos.append(evento)

        return eventos
