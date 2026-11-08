import logging
from flask import jsonify, request
from ..Dao.UsuarioMinisterioDao import UsuarioMinisterioDao
from ..Dao.UsuariosDao import UsuariosDao
from ..Dao.MinisterioDao import MinisterioDao
from ..Models.UsuarioMinisterio import UsuarioMinisterio
from ..Http.ErrorResponse import ErrorResponse
from datetime import datetime

class UsuarioMinisterioController:
    def __init__(self, usuario_ministerio_dao: UsuarioMinisterioDao, usuarios_dao: UsuariosDao, ministerio_dao: MinisterioDao):
        self.dao = usuario_ministerio_dao
        self.u_dao = usuarios_dao
        self.m_dao = ministerio_dao
        logging.info("⬆️ UsuarioMinisterioController::__init__")

    def create(self, req):
        logging.info("🔵 UsuarioMinisterioController::create")
        corpo = req.get_json()

        # Suporta aninhamento 'inscricao' ou raiz
        insc = corpo.get("inscricao", corpo) if isinstance(corpo, dict) else {}

        uid = insc.get("idUsuario") or corpo.get("idUsuario")
        mid = insc.get("idMinisterio") or corpo.get("idMinisterio")
        funcao = insc.get("funcao") or corpo.get("funcao", "Membro")
        data_entrada = insc.get("dataEntrada") or corpo.get("dataEntrada", datetime.now().strftime("%Y-%m-%d"))

        if not uid or not mid:
            raise ErrorResponse(400, "Campos obrigatórios", {"message": "idUsuario e idMinisterio obrigatórios"})

        if not self.u_dao.find_by_id(int(uid)):
            raise ErrorResponse(400, "Usuário não encontrado", {})

        if not self.m_dao.find_by_id(int(mid)):
            raise ErrorResponse(400, "Ministério não encontrado", {})

        if self.dao.exists(int(uid), int(mid)):
            raise ErrorResponse(400, "Já inscrito", {"message": "Usuário já está neste ministério"})

        vinculo = UsuarioMinisterio()
        vinculo.set_id_usuario(int(uid))
        vinculo.set_id_ministerio(int(mid))
        vinculo.set_funcao(funcao)
        vinculo.set_data_entrada(data_entrada)

        vinculo_criado = self.dao.create(vinculo)

        return jsonify({"success": True, "data": vinculo_criado.to_dict()}), 201

    def find_all(self, req):
        logging.info("🔵 UsuarioMinisterioController::find_all")
        lista = self.dao.find_all()
        return jsonify({"success": True, "data": {"vinculos": [v.to_dict() for v in lista]}}), 200

    def delete(self, req, id_vinculo):
        logging.info("🔵 UsuarioMinisterioController::delete")
        ok = self.dao.delete(int(id_vinculo))
        return jsonify({"success": ok}), (200 if ok else 404)
