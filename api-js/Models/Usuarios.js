class Usuarios {
    constructor() {
        this.idUsuario = 0;
        this.nomeUsuario = "";
        this.email = "";
        this.senha = "";
        this.tel = "";
        this.tipoUsuario = "";
        this.dataNasc = "";
    }

    getIdUsuario() {
        return this.idUsuario;
    }

    setIdUsuario(value) {
        if (value <= 0) {
            throw new Error("idUsuario deve ser maior que zero.");
        }
        this.idUsuario = value;
    }

    getIdUsuarios() {
        return this.getIdUsuario();
    }

    setIdUsuarios(value) {
        this.setIdUsuario(value);
    }

    getNomeUsuario() {
        return this.nomeUsuario;
    }

    setNomeUsuario(value) {
        const nome = value.trim();
        if (nome === "") {
            throw new Error("nomeUsuario nao pode ser vazio.");
        }
        if (nome.length < 3) {
            throw new Error("nomeUsuario deve ter pelo menos 3 caracteres.");
        }
        if (nome.length > 100) {
            throw new Error("nomeUsuario muito grande.");
        }
        this.nomeUsuario = nome;
    }

    getNome() {
        return this.getNomeUsuario();
    }

    setEmail(email) {
        const emailTrimmed = email.trim();
        if (emailTrimmed === "") {
            throw new Error("email nao pode ser vazio.");
        }
        // Validação simples de email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailTrimmed)) {
            throw new Error("email invalido.");
        }
        this.email = emailTrimmed;
    }

    getEmail() {
        return this.email;
    }

    setSenha(senha) {
        if (senha.trim() === "") {
            throw new Error("senha nao pode ser vazia.");
        }
        this.senha = senha;
    }

    getSenha() {
        return this.senha;
    }

    setTel(tel) {
        this.tel = tel ? tel.trim() : "";
    }

    getTel() {
        return this.tel;
    }

    setTipoUsuario(tipoUsuario) {
        this.tipoUsuario = tipoUsuario ? tipoUsuario.trim() : "";
    }

    getTipoUsuario() {
        return this.tipoUsuario;
    }

    setDataNasc(dataNasc) {
        if (!dataNasc) {
            this.dataNasc = "";
            return;
        }

        // mysql2 retorna colunas DATE como objetos Date.
        if (dataNasc instanceof Date) {
            this.dataNasc = dataNasc.toISOString().slice(0, 10);
            return;
        }

        this.dataNasc = String(dataNasc).trim();
    }

    getDataNasc() {
        return this.dataNasc;
    }

    toJSON() {
        return {
            idUsuario: this.getIdUsuario(),
            nomeUsuario: this.getNomeUsuario(),
            email: this.getEmail(),
            tel: this.getTel(),
            tipoUsuario: this.getTipoUsuario(),
            data_nasc: this.getDataNasc(),
        };
    }
}

module.exports = Usuarios;
