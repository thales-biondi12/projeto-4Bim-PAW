class UsuarioMinisterio {
    constructor() {
        this.id = null;
        this.idUsuario = null;
        this.idMinisterio = null;
        this.dataEntrada = "";
        this.funcao = "";
        this.nomeUsuario = null;
        this.nomeMinisterio = null;
    }

    getId() {
        return this.id;
    }

    setId(v) {
        this.id = v;
    }

    getIdUsuario() {
        return this.idUsuario;
    }

    setIdUsuario(v) {
        this.idUsuario = v;
    }

    getIdMinisterio() {
        return this.idMinisterio;
    }

    setIdMinisterio(v) {
        this.idMinisterio = v;
    }

    getDataEntrada() {
        return this.dataEntrada;
    }

    setDataEntrada(v) {
        this.dataEntrada = v;
    }

    getFuncao() {
        return this.funcao;
    }

    setFuncao(v) {
        this.funcao = v;
    }

    getNomeUsuario() {
        return this.nomeUsuario;
    }

    setNomeUsuario(v) {
        this.nomeUsuario = v;
    }

    getNomeMinisterio() {
        return this.nomeMinisterio;
    }

    setNomeMinisterio(v) {
        this.nomeMinisterio = v;
    }

    toJSON() {
        return {
            id: this.id,
            idUsuario: this.idUsuario,
            idMinisterio: this.idMinisterio,
            dataEntrada: this.dataEntrada,
            funcao: this.funcao,
            nomeUsuario: this.nomeUsuario,
            nomeMinisterio: this.nomeMinisterio,
        };
    }
}

module.exports = UsuarioMinisterio;
