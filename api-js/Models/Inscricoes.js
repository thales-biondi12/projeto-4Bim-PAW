class Inscricoes {
    constructor() {
        this.idInscricoes = null;
        this.usuarioId = null;
        this.eventoId = null;
        this.dataInscricao = "";
        this.presenca = "";
        this.nomeUsuario = null;
        this.tituloEvento = null;
    }

    getIdInscricoes() {
        return this.idInscricoes;
    }

    setIdInscricoes(value) {
        if (value <= 0) {
            throw new Error("idInscricoes deve ser maior que zero.");
        }
        this.idInscricoes = value;
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

    getEventoId() {
        return this.eventoId;
    }

    setEventoId(value) {
        if (value <= 0) {
            throw new Error("eventoId deve ser maior que zero.");
        }
        this.eventoId = value;
    }

    getDataInscricao() {
        return this.dataInscricao;
    }

    setDataInscricao(value) {
        if (!value) {
            throw new Error("dataInscricao nao pode ser vazia.");
        }
        const data = value instanceof Date
            ? value.toISOString().slice(0, 10)
            : String(value).trim();
        if (data === "") {
            throw new Error("dataInscricao nao pode ser vazia.");
        }
        this.dataInscricao = data;
    }

    getPresenca() {
        return this.presenca;
    }

    setPresenca(value) {
        const presenca = String(value ?? '').trim();
        if (presenca === "") {
            throw new Error("presenca nao pode ser vazia.");
        }
        this.presenca = presenca;
    }

    getNomeUsuario() {
        return this.nomeUsuario;
    }

    setNomeUsuario(v) {
        this.nomeUsuario = v;
    }

    getTituloEvento() {
        return this.tituloEvento;
    }

    setTituloEvento(v) {
        this.tituloEvento = v;
    }

    toJSON() {
        return {
            idInscricoes: this.getIdInscricoes(),
            usuarioId: this.getUsuarioId(),
            eventoId: this.getEventoId(),
            dataInscricao: this.getDataInscricao(),
            presenca: this.getPresenca(),
            nomeUsuario: this.getNomeUsuario(),
            tituloEvento: this.getTituloEvento(),
        };
    }
}

module.exports = Inscricoes;
