class ErrorResponse(Exception):
    """
    Classe personalizada de erro para a aplicação.

    Permite incluir:
    - Código HTTP (http_code)
    - Informações adicionais sobre o erro (error)
    """
    def __init__(self, http_code: int, message: str, error=None):
        super().__init__(message)
        self.http_code = http_code
        self.error = error
        self.name = "ErrorResponse"

    def get_http_code(self) -> int:
        return self.http_code

    def get_error(self):
        return self.error

    def get_name(self) -> str:
        return self.name
