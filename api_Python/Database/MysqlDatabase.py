import mysql.connector
from mysql.connector import Error
import logging
import os

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

        # Permite configurar a API sem alterar o código.  Os nomes com
        # MYSQL_* são compatíveis com instalações locais e Docker.
        self.host = config.get("host") or os.getenv("MYSQL_HOST", "127.0.0.1")
        self.user = config.get("user") or os.getenv("MYSQL_USER", "root")
        self.password = config.get("password") if "password" in config else os.getenv("MYSQL_PASSWORD", "")
        self.database = config.get("database") or os.getenv("MYSQL_DATABASE", "web")
        self.port = int(config.get("port") or os.getenv("MYSQL_PORT", "3306"))

    def get_connection(self):
        """
        Retorna a conexão MySQL singleton.

        Returns:
            mysql.connector.connection.MySQLConnection
        Raises:
            Exception: Se houver falha na conexão.
        """
        # Reabre a conexão quando o MySQL encerra o singleton por inatividade.
        if MysqlDatabase._connection is not None:
            try:
                if MysqlDatabase._connection.is_connected():
                    return MysqlDatabase._connection
            except Exception:
                pass
            try:
                MysqlDatabase._connection.close()
            except Exception:
                pass
            MysqlDatabase._connection = None

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
