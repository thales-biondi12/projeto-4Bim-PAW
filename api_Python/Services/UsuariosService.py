import logging
import hashlib
try:
    import bcrypt
except ModuleNotFoundError:
    bcrypt = None
from typing import List, Optional, Any
from ..Models.Usuarios import Usuarios
from ..Dao.UsuariosDao import UsuariosDao
from ..Http.ErrorResponse import ErrorResponse

def hash_password(password: str) -> str:
    """Simulação de password_hash do PHP (Bcrypt) usando hashlib/sha256 para simplicidade,
    embora em produção deva-se usar bcrypt ou argon2."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verifica se a senha coincide com o hash."""
    return hash_password(password) == hashed

def verify_bcrypt_password(password: str, hashed: str) -> bool:
    if bcrypt is None:
        return False
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except (ValueError, TypeError):
        return False

class UsuariosService:
    def __init__(self, usuarios_dao_dep: UsuariosDao):
        self.usuarios_dao = usuarios_dao_dep
        logging.info("⬆️ UsuariosService::__init__")

    def create_service(self, data: Any) -> Usuarios:
        logging.info("🟣 UsuariosService::create_service")

        dados = data.get("usuarios") or data.get("usuario") if isinstance(data, dict) else \
                getattr(data, "usuarios", getattr(data, "usuario", None))

        if not dados:
            raise ErrorResponse(400, "Dados inválidos", {"message": "Objeto 'usuarios' é obrigatório"})

        usuario = Usuarios()
        nome_u = (dados.get("nomeUsuario") or dados.get("nome", "")) if isinstance(dados, dict) else \
                (getattr(dados, "nomeUsuario", getattr(dados, "nome", "")))
        usuario.set_nome_usuario(nome_u)

        email = dados.get("email") if isinstance(dados, dict) else getattr(dados, "email", "")
        usuario.set_email(email)

        senha_pura = dados.get("senha") if isinstance(dados, dict) else getattr(dados, "senha", "")
        usuario.set_senha(hash_password(senha_pura))

        usuario.set_tel(dados.get("tel") if isinstance(dados, dict) else getattr(dados, "tel", None))

        tipo_u = (dados.get("tipoUsuario") or dados.get("tipo_usuario", "MEMBRO")) if isinstance(dados, dict) else \
                 (getattr(dados, "tipoUsuario", getattr(dados, "tipo_usuario", "MEMBRO")))
        usuario.set_tipo_usuario(tipo_u)

        data_n = (dados.get("data_nasc") or dados.get("dataNasc")) if isinstance(dados, dict) else \
                 (getattr(dados, "data_nasc", getattr(dados, "dataNasc", None)))
        usuario.set_data_nasc(data_n)

        resultado = self.usuarios_dao.find_by_field("email", usuario.get_email())
        if len(resultado) > 0:
            raise ErrorResponse(400, "Usuário já existe", {"message": f"O email {usuario.get_email()} já está cadastrado"})

        return self.usuarios_dao.create(usuario)

    def login_service(self, data: Any) -> Usuarios:
        logging.info("🟣 UsuariosService::login_service")

        dados = data.get("usuarios") or data.get("usuario") or data.get("funcionario") if isinstance(data, dict) else \
                getattr(data, "usuarios", getattr(data, "usuario", getattr(data, "funcionario", None)))

        if not dados or not (dados.get("email") if isinstance(dados, dict) else getattr(dados, "email", None)) or \
           not (dados.get("senha") if isinstance(dados, dict) else getattr(dados, "senha", None)):
            raise ErrorResponse(400, "Dados inválidos", {"message": "Email e senha são obrigatórios"})

        email = (dados.get("email") if isinstance(dados, dict) else getattr(dados, "email", "")).strip()
        senha_informada = (dados.get("senha") if isinstance(dados, dict) else getattr(dados, "senha", ""))

        resultado = self.usuarios_dao.find_by_field("email", email)
        if not resultado:
            raise ErrorResponse(401, "Credenciais inválidas", {"message": "Email ou senha incorretos"})

        usuario = resultado[0]
        senha_banco = str(usuario.get_senha())

        # Verifica se a senha é hash ou texto puro (compatibilidade)
        # Se o hash for sha256 (nosso padrão aqui), terá 64 caracteres
        if senha_banco.startswith(("$2a$", "$2b$", "$2y$")):
            senha_valida = verify_bcrypt_password(senha_informada, senha_banco)
        elif len(senha_banco) == 64:
            senha_valida = verify_password(senha_informada, senha_banco)
        else:
            # Senha em texto puro
            senha_valida = (senha_banco == senha_informada)
            if senha_valida:
                # Migra para hash
                usuario.set_senha(hash_password(senha_informada))
                self.usuarios_dao.update(usuario)

        if not senha_valida:
            raise ErrorResponse(401, "Credenciais inválidas", {"message": "Email ou senha incorretos"})

        return usuario

    def count_service(self) -> int:
        logging.info("🟣 UsuariosService::count_service")
        return self.usuarios_dao.count()

    def find_all_service(self) -> List[Usuarios]:
        logging.info("🟣 UsuariosService::find_all_service")
        return self.usuarios_dao.find_all()

    def find_by_id_service(self, id_usuario: int) -> Optional[Usuarios]:
        logging.info("🟣 UsuariosService::find_by_id_service")
        return self.usuarios_dao.find_by_id(id_usuario)

    def update_service(self, id_usuario: int, data: Any) -> Usuarios:
        logging.info("🟣 UsuariosService::update_service")

        usuario_existente = self.usuarios_dao.find_by_id(id_usuario)
        if not usuario_existente:
            raise ErrorResponse(404, "Usuário não encontrado", {"message": f"Não existe usuário com id {id_usuario}"})

        dados = data.get("usuarios") or data.get("usuario") if isinstance(data, dict) else \
                getattr(data, "usuarios", getattr(data, "usuario", None))
        if not dados:
            raise ErrorResponse(400, "Dados inválidos", {"message": "Objeto 'usuarios' é obrigatório"})

        nome_u = (dados.get("nomeUsuario") or dados.get("nome")) if isinstance(dados, dict) else \
                (getattr(dados, "nomeUsuario", getattr(dados, "nome", None)))
        if nome_u:
            usuario_existente.set_nome_usuario(nome_u)

        email = dados.get("email") if isinstance(dados, dict) else getattr(dados, "email", None)
        if email:
            usuario_existente.set_email(email)

        senha = dados.get("senha") if isinstance(dados, dict) else getattr(dados, "senha", None)
        if senha and senha.strip():
            usuario_existente.set_senha(hash_password(senha))

        tel = dados.get("tel") if isinstance(dados, dict) else getattr(dados, "tel", None)
        if tel is not None:
            usuario_existente.set_tel(tel)

        tipo_u = (dados.get("tipoUsuario") or dados.get("tipo_usuario")) if isinstance(dados, dict) else \
                 (getattr(dados, "tipoUsuario", getattr(dados, "tipo_usuario", None)))
        if tipo_u:
            usuario_existente.set_tipo_usuario(tipo_u)

        data_n = (dados.get("data_nasc") or dados.get("dataNasc")) if isinstance(dados, dict) else \
                 (getattr(dados, "data_nasc", getattr(dados, "dataNasc", None)))
        if data_n:
            usuario_existente.set_data_nasc(data_n)

        self.usuarios_dao.update(usuario_existente)
        return usuario_existente

    def delete_service(self, id_usuario: int) -> bool:
        logging.info("🟣 UsuariosService::delete_service")
        usuario_existente = self.usuarios_dao.find_by_id(id_usuario)
        if not usuario_existente:
            raise ErrorResponse(404, "Usuário não encontrado", {"message": f"Não existe usuário com id {id_usuario}"})

        return self.usuarios_dao.delete(usuario_existente)
