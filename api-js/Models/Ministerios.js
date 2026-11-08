class Ministerios {
    constructor() {
        this.idMinisterios = null;
        this.nome = "";
        this.descricao = "";
        this.diaReuniao = "";
        this.idCoordenador = null;
        this.nomeCoordenador = null;
    }

    getIdMinisterios() {
        return this.idMinisterios;
    }

    setIdMinisterios(value) {
        if (value <= 0) {
            throw new Error("idMinisterios deve ser maior que zero.");
        }
        this.idMinisterios = value;
    }

    getNome() {
        return this.nome;
    }

    setNome(value) {
        const nome = value.trim();
        if (nome === "") {
            throw new Error("nome nao pode ser vazio.");
        }
        if (nome.length < 3) {
            throw new Error("nome deve ter pelo menos 3 caracteres.");
        }
        if (nome.length > 100) {
            throw new Error("nome muito grande.");
        }
        this.nome = nome;
    }

    getDescricao() {
        return this.descricao;
    }

    setDescricao(value) {
        this.descricao = value ? value.trim() : "";
    }

    getDiaReuniao() {
        return this.diaReuniao;
    }

    setDiaReuniao(value) {
        const dia = value.trim();
        if (dia === "") {
            throw new Error("diaReuniao nao pode ser vazio.");
        }
        this.diaReuniao = dia;
    }

    getIdCoordenador() {
        return this.idCoordenador;
    }

    setIdCoordenador(value) {
        if (value <= 0) {
            throw new Error("idCoordenador deve ser maior que zero.");
        }
        this.idCoordenador = value;
    }

    getNomeCoordenador() {
        return this.nomeCoordenador;
    }

    setNomeCoordenador(v) {
        this.nomeCoordenador = v;
    }

    toJSON() {
        return {
            idMinisterios: this.getIdMinisterios(),
            nome: this.getNome(),
            descricao: this.getDescricao(),
            diaReuniao: this.getDiaReuniao(),
            idCoordenador: this.getIdCoordenador(),
            nomeCoordenador: this.getNomeCoordenador(),
        };
    }
}

module.exports = Ministerios;
