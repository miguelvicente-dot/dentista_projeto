from flask import request, jsonify
import sqlite3
from .models import Paciente, Consulta
from .dao import PacienteDAO, ConsultaDAO

def registrar_rotas(app):
    """Rotas da API: recebem e devolvem JSON (usadas pelo JavaScript com Fetch)."""
    paciente_dao = PacienteDAO()
    consulta_dao = ConsultaDAO()

    def dados_paciente(dados):
        return Paciente(
            nome=(dados.get("nome") or "").strip(),
            telefone=(dados.get("telefone") or "").strip(),
            email=(dados.get("email") or "").strip(),
            cpf=(dados.get("cpf") or "").strip() or None,  # vazio vira NULL (o CPF é UNIQUE)
            data_nascimento=dados.get("data_nascimento") or "",
            endereco=(dados.get("endereco") or "").strip()
        )

    @app.get("/api/pacientes")
    def listar_pacientes():
        return jsonify([p.para_dict() for p in paciente_dao.listar()])

    @app.post("/api/pacientes")
    def cadastrar_paciente():
        dados = request.get_json(silent=True) or {}
        if not dados.get("nome") or not dados.get("telefone"):
            return jsonify({"erro": "Nome e telefone são obrigatórios."}), 400
        try:
            paciente = paciente_dao.cadastrar(dados_paciente(dados))
            return jsonify({"mensagem": "Paciente cadastrado!", "paciente": paciente.para_dict()}), 201
        except sqlite3.IntegrityError:
            return jsonify({"erro": "Este CPF já está cadastrado."}), 409

    @app.put("/api/pacientes/<int:paciente_id>")
    def editar_paciente(paciente_id):
        dados = request.get_json(silent=True) or {}
        if not dados.get("nome") or not dados.get("telefone"):
            return jsonify({"erro": "Nome e telefone são obrigatórios."}), 400
        try:
            atualizado = paciente_dao.atualizar(paciente_id, dados_paciente(dados))
            if not atualizado:
                return jsonify({"erro": "Paciente não encontrado."}), 404
            return jsonify({"mensagem": "Cadastro atualizado!"})
        except sqlite3.IntegrityError:
            return jsonify({"erro": "Este CPF já está cadastrado."}), 409

    @app.delete("/api/pacientes/<int:paciente_id>")
    def excluir_paciente(paciente_id):
        if not paciente_dao.excluir(paciente_id):
            return jsonify({"erro": "Paciente não encontrado."}), 404
        return jsonify({"mensagem": "Paciente excluído."})

    @app.get("/api/consultas")
    def listar_consultas():
        return jsonify(consulta_dao.listar())

    @app.post("/api/consultas")
    def cadastrar_consulta():
        dados = request.get_json(silent=True) or {}
        obrigatorios = ["paciente_id", "data", "horario", "procedimento"]
        if any(not dados.get(campo) for campo in obrigatorios):
            return jsonify({"erro": "Preencha paciente, data, horário e procedimento."}), 400
        try:
            consulta = Consulta(
                paciente_id=int(dados["paciente_id"]),
                data=dados["data"],
                horario=dados["horario"],
                procedimento=dados["procedimento"],
                observacoes=dados.get("observacoes", "")
            )
            consulta_dao.cadastrar(consulta)
            return jsonify({"mensagem": "Consulta agendada!"}), 201
        except (ValueError, sqlite3.IntegrityError):
            return jsonify({"erro": "Paciente inválido. Confira o cadastro."}), 400

    @app.put("/api/consultas/<int:consulta_id>/status")
    def mudar_status_consulta(consulta_id):
        dados = request.get_json(silent=True) or {}
        status = dados.get("status")
        if status not in Consulta.STATUS_VALIDOS:
            return jsonify({"erro": "Situação inválida."}), 400
        if not consulta_dao.atualizar_status(consulta_id, status):
            return jsonify({"erro": "Consulta não encontrada."}), 404
        return jsonify({"mensagem": f"Consulta marcada como {status}."})

    @app.delete("/api/consultas/<int:consulta_id>")
    def excluir_consulta(consulta_id):
        if not consulta_dao.excluir(consulta_id):
            return jsonify({"erro": "Consulta não encontrada."}), 404
        return jsonify({"mensagem": "Consulta excluída."})
