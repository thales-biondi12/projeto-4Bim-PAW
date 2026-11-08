import mysql.connector
from mysql.connector import Error
import logging

class MysqlDatabase:
    """
    Classe responsável por gerenciar a conexão com o banco MySQL.

    - Suporta passagem de dados de conexão via construtor.
    - Mantém um singleton de conexão para reutilização.
    """
    _connection = None

    def __init__(self, config=None):
        if config is None:
            config = {}

        self.host = config.get("host", "127.0.0.1")
        self.user = config.get("user", "root")
        self.password = config.get("password", "")
        self.database = config.get("database", "Web")
        self.port = config.get("port", 3306)

    def get_connection(self):
        """
        Retorna a conexão MySQL singleton.

        Returns:
            mysql.connector.connection.MySQLConnection
        Raises:
            Exception: Se houver falha na conexão.
        """
        if MysqlDatabase._connection is None:
            try:
                MysqlDatabase._connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    charset='utf8mb4',
                    use_pure=True
                )
                logging.info("⬆️ Conectado ao MySQL com sucesso!")
            except Error as e:
                logging.error(f"❌ Falha ao conectar ao MySQL: {e}")
                raise Exception(f"Falha ao conectar ao MySQL: {e}")

        return MysqlDatabase._connection
