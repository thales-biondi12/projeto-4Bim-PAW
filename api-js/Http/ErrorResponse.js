class ErrorResponse extends Error {
    constructor(httpCode, message, error = null) {
        super(message);
        this.name = "ErrorResponse";
        this.httpCode = httpCode;
        this.error = error;

        // Garante que o stack trace seja preservado
        Error.captureStackTrace(this, this.constructor);
    }

    getHttpCode() {
        return this.httpCode;
    }

    getError() {
        return this.error;
    }
}

module.exports = ErrorResponse;
