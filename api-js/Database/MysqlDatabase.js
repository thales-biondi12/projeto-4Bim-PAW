const mysql = require('mysql2/promise');

/**
 * Classe responsável por gerenciar a conexão com o banco MySQL.
 *
 * - Suporta passagem de dados de conexão via construtor.
 * - Mantém um singleton de pool de conexão para reutilização.
 */
class MysqlDatabase {
    /** @var Pool|null Pool de conexão singleton */
    static connection = null;

    /** @var string Configurações do banco */
    /**
     * Construtor recebe dados de conexão.
     *
     * @param Object config
     * Exemplo:
     * {
     *   host: '127.0.0.1',
     *   user: 'root',
     *   password: '',
     *   database: 'Web',
     *   port: 3306
     * }
     */
    constructor(config = {}) {
        this.host = config.host || '127.0.0.1';
        this.user = config.user || 'root';
        this.password = config.password || '';
        this.database = config.database || 'Web';
        this.port = config.port || 3306;
    }

    /**
     * Retorna a conexão do pool singleton.
     *
     * @returns Promise<Pool>
     * @throws Error
     */
    async getConnection() {
        if (MysqlDatabase.connection === null) {
            try {
                MysqlDatabase.connection = mysql.createPool({
                    host: this.host,
                    user: this.user,
                    password: this.password,
                    database: this.database,
                    port: this.port,
                    waitForConnections: true,
                    connectionLimit: 10,
                    queueLimit: 0
                });
                console.log("⬆️  Conectado ao MySQL com sucesso!");
            } catch (e) {
                console.error("❌ Falha ao conectar ao MySQL: " + e.message);
                throw new Error(
                    "Falha ao conectar ao MySQL: " + e.message
                );
            }
        }

        return MysqlDatabase.connection;
    }
}

module.exports = MysqlDatabase;
