const jwt = require('jsonwebtoken');
const crypto = require('crypto');

/**
 * Classe responsável pela geração e validação de tokens JWT.
 */
class MeuTokenJWT {
    // Chave secreta utilizada para assinar e validar os tokens.
    static KEY = "x9S4q0v+V0IjvHkG20uAxaHx1ijj+q1HWjHKv+ohxp/oK+77qyXkVj/l4QYHHTF3";
    static ALGORITHM = "HS256";
    static TYPE = "JWT";

    constructor() {
        this.payload = null;
        this.iss = "http://localhost";
        this.aud = "http://localhost";
        this.sub = "acesso_sistema";
        // 30 dias
        this.duration = 3600 * 24 * 30;
    }

    /**
     * Gera um token JWT.
     * @param Object claims
     * @returns string
     */
    gerarToken(claims) {
        // Normaliza claims para suportar ambos os padrões (Novo e Legado)
        const idUsuario = claims.idUsuario || claims.idFuncionario || claims.id || null;
        const nome = claims.nomeUsuario || claims.name || claims.nome || null;
        const email = claims.email || null;
        const tipo = claims.tipoUsuario || claims.role || claims.tipo_usuario || null;

        const dadosUsuario = {
            idUsuario: idUsuario,
            nomeUsuario: nome,
            email: email,
            tipoUsuario: tipo,
        };

        const dadosFuncionario = {
            idFuncionario: idUsuario,
            idUsuario: idUsuario,
            name: nome,
            nomeUsuario: nome,
            email: email,
            role: tipo,
            tipoUsuario: tipo,
        };

        const payload = {
            iss: this.iss,
            aud: this.aud,
            sub: this.sub,
            iat: Math.floor(Date.now() / 1000),
            nbf: Math.floor(Date.now() / 1000),
            exp: Math.floor(Date.now() / 1000) + this.duration,
            jti: crypto.randomBytes(16).toString('hex'),
            usuario: dadosUsuario,
            funcionario: dadosFuncionario,
        };

        return jwt.sign(payload, MeuTokenJWT.KEY, {
            algorithm: MeuTokenJWT.ALGORITHM,
            header: { typ: MeuTokenJWT.TYPE }
        });
    }

    /**
     * Valida um token JWT.
     * @param string stringToken
     * @returns boolean
     */
    validateToken(stringToken) {
        if (!stringToken) return false;

        let token = stringToken.trim();
        if (token.startsWith("Bearer ")) {
            token = token.substring(7);
        }

        // Verifica formato básico: header.payload.signature
        const pattern = /^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+$/;
        if (!pattern.test(token)) return false;

        try {
            const decoded = jwt.verify(token, MeuTokenJWT.KEY, {
                algorithms: [MeuTokenJWT.ALGORITHM]
            });

            // Valida ISS, AUD e SUB
            if (decoded.iss !== this.iss || decoded.aud !== this.aud || decoded.sub !== this.sub) {
                return false;
            }

            this.payload = decoded;
            return true;
        } catch (e) {
            return false;
        }
    }

    getPayload() {
        return this.payload;
    }

    setPayload(payload) {
        this.payload = payload;
        return this;
    }

    limparPayload() {
        this.payload = null;
        return this;
    }

    getIss() { return this.iss; }
    setIss(iss) { this.iss = iss; return this; }
    getAud() { return this.aud; }
    setAud(aud) { this.aud = aud; return this; }
    getSub() { return this.sub; }
    setSub(sub) { this.sub = sub; return this; }
    getDuration() { return this.duration; }
    setDuration(duration) { this.duration = duration; return this; }
}

module.exports = MeuTokenJWT;
