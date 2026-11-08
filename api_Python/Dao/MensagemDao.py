import logging
from typing import List, Optional, Any
from ..Models.Mensagens import Mensagens
from ..Database.MysqlDatabase import MysqlDatabase

class MensagemDao:
    """
    Classe responsável pelo acesso aos dados da entidade Mensagens.
    """
    def __init__(self, database_instance: MysqlDatabase):
        self.database = database_instance
        logging.info("⬆️ MensagemDao::__init__")

    def create(self, obj_mensagem: Mensagens) -> Mensagens:
        logging.info("🟢 MensagemDao::create")
        sql = """
            INSERT INTO mensagens
            (titulo, conteudo, usuario_id, data_postagem)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            obj_mensagem.get_titulo(),
            obj_mensagem.get_conteudo(),
            obj_mensagem.get_usuario_id(),
            obj_mensagem.get_data_postagem()
        )

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        obj_mensagem.set_id_mensagens(cursor.lastrowid)
        return obj_mensagem

    def delete(self, obj_mensagem_model: Mensagens) -> bool:
        logging.info("🟢 MensagemDao::delete")
        sql = "DELETE FROM mensagens WHERE id_mensagens = %s"
        params = (obj_mensagem_model.get_id_mensagens(),)

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        return cursor.rowcount > 0

    def update(self, obj_mensagem_model: Mensagens) -> bool:
        logging.info("🟢 MensagemDao::update")
        sql = """
            UPDATE mensagens
            SET titulo = %s, conteudo = %s, usuario_id = %s, data_postagem = %s
            WHERE id_mensagens = %s
        """
        params = (
            obj_mensagem_model.get_titulo(),
            obj_mensagem_model.get_conteudo(),
            obj_mensagem_model.get_usuario_id(),
            obj_mensagem_model.get_data_postagem(),
            obj_mensagem_model.get_id_mensagens()
        )

        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        return cursor.rowcount > 0

    def find_all(self) -> List[Mensagens]:
        logging.info("🟢 MensagemDao::find_all")
        sql = "SELECT * FROM mensagens"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()

        mensagens = []
        for row in rows:
            mensagem = Mensagens()
            mensagem.set_id_mensagens(int(row["id_mensagens"]))
            mensagem.set_titulo(row["titulo"])
            mensagem.set_conteudo(row["conteudo"])
            mensagem.set_usuario_id(int(row["usuario_id"]))
            mensagem.set_data_postagem(row["data_postagem"])
            mensagens.append(mensagem)

        return mensagens

    def count(self) -> int:
        logging.info("🟢 MensagemDao::count")
        sql = "SELECT COUNT(*) AS qtd FROM mensagens"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        row = cursor.fetchone()

        return int(row["qtd"]) if row else 0

    def find_by_id(self, id_mensagens: int) -> Optional[Mensagens]:
        logging.info("🟢 MensagemDao::find_by_id")
        resultado = self.find_by_field("id_mensagens", id_mensagens)
        return resultado[0] if resultado else None

    def find_by_field(self, field: str, value: Any) -> List[Mensagens]:
        logging.info("🟢 MensagemDao::find_by_field")
        campos_permitidos = ["id_mensagens", "titulo", "conteudo", "usuario_id", "data_postagem"]

        if field not in campos_permitidos:
            raise Exception("Campo inválido.")

        sql = f"SELECT * FROM mensagens WHERE {field} = %s"

        conn = self.database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (value,))
        rows = cursor.fetchall()

        mensagens = []
        for row in rows:
            mensagem = Mensagens()
            mensagem.set_id_mensagens(int(row["id_mensagens"]))
            mensagem.set_titulo(row["titulo"])
            mensagem.set_conteudo(row["conteudo"])
            mensagem.set_usuario_id(int(row["usuario_id"]))
            mensagem.set_data_postagem(row["data_postagem"])
            mensagens.append(mensagem)

        return mensagens
