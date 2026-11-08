class Mensagens {
    constructor() {
        this.idMensagens = null;
        this.titulo = "";
        this.conteudo = "";
        this.usuarioId = null;
        this.dataPostagem = "";
    }

    getIdMensagens() {
        return this.idMensagens;
    }

    setIdMensagens(value) {
        if (value <= 0) {
            throw new Error("idMensagens deve ser maior que zero.");
        }
        this.idMensagens = value;
    }

    getTitulo() {
        return this.titulo;
    }

    setTitulo(value) {
        const titulo = value.trim();
        if (titulo === "") {
            throw new Error("titulo nao pode ser vazio.");
        }
        if (titulo.length < 3) {
            throw new Error("titulo deve ter pelo menos 3 caracteres.");
        }
        if (titulo.length > 100) {
            throw new Error("titulo muito grande.");
        }
        this.titulo = titulo;
    }

    getConteudo() {
        return this.conteudo;
    }

    setConteudo(value) {
        const conteudo = value.trim();
        if (conteudo === "") {
            throw new Error("conteudo nao pode ser vazio.");
        }
        this.conteudo = conteudo;
    }

    getUsuarioId() {
        return this.usuarioId;
    }

    setUsuarioId(value) {
        if (value <= 0) {
            throw new Error("usuarioId deve ser maior que zero.");
        }
        this.usuarioId = value;
    }

    getDataPostagem() {
        return this.dataPostagem;
    }

    setDataPostagem(value) {
        if (!value) {
            throw new Error("dataPostagem nao pode ser vazia.");
        }

        // mysql2 retorna colunas DATE/DATETIME como objetos Date.
        const data = value instanceof Date
            ? value.toISOString().slice(0, 10)
            : String(value).trim();
        if (data === "") {
            throw new Error("dataPostagem nao pode ser vazia.");
        }
        this.dataPostagem = data;
    }

    toJSON() {
        return {
            idMensagens: this.getIdMensagens(),
            titulo: this.getTitulo(),
            conteudo: this.getConteudo(),
            usuarioId: this.getUsuarioId(),
            dataPostagem: this.getDataPostagem(),
        };
    }
}

module.exports = Mensagens;
