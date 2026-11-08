class Eventos {
    constructor() {
        this.idEvento = null;
        this.titulo = "";
        this.descricao = "";
        this.dataEvento = "";
        this.localEvento = "";
        this.limiteVagas = null;
        this.statusEvento = "";
    }

    getIdEvento() {
        return this.idEvento;
    }

    setIdEvento(value) {
        if (value <= 0) {
            throw new Error("idEvento deve ser maior que zero.");
        }
        this.idEvento = value;
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

    getDescricao() {
        return this.descricao;
    }

    setDescricao(value) {
        const descricao = value.trim();
        if (descricao === "") {
            throw new Error("descricao nao pode ser vazia.");
        }
        this.descricao = descricao;
    }

    getDataEvento() {
        return this.dataEvento;
    }

    setDataEvento(value) {
        // mysql2 retorna DATE/DATETIME como objeto Date por padrão.
        const data = value instanceof Date
            ? value.toISOString().slice(0, 19)
            : String(value ?? '').trim();
        if (data === "") {
            throw new Error("dataEvento nao pode ser vazia.");
        }
        this.dataEvento = data;
    }

    getLocalEvento() {
        return this.localEvento;
    }

    setLocalEvento(value) {
        const local = value.trim();
        if (local === "") {
            throw new Error("localEvento nao pode ser vazio.");
        }
        this.localEvento = local;
    }

    getLimiteVagas() {
        return this.limiteVagas;
    }

    setLimiteVagas(value) {
        if (value < 0) {
            throw new Error("limiteVagas nao pode ser negativo.");
        }
        this.limiteVagas = value;
    }

    getStatusEvento() {
        return this.statusEvento;
    }

    setStatusEvento(value) {
        const status = value.trim();
        if (status === "") {
            throw new Error("statusEvento nao pode ser vazio.");
        }
        this.statusEvento = status;
    }

    toJSON() {
        return {
            idEvento: this.getIdEvento(),
            titulo: this.getTitulo(),
            descricao: this.getDescricao(),
            dataEvento: this.getDataEvento(),
            localEvento: this.getLocalEvento(),
            limiteVagas: this.getLimiteVagas(),
            statusEvento: this.getStatusEvento(),
        };
    }
}

module.exports = Eventos;
