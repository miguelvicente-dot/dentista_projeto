from datetime import date
from flask import render_template, abort
from .dao import PacienteDAO, ConsultaDAO

def registrar_paginas(app):
    """Rotas das páginas: devolvem HTML montado com os templates (Jinja)."""
    paciente_dao = PacienteDAO()
    consulta_dao = ConsultaDAO()

    @app.route("/")
    def inicio():
        # O Python busca os números no banco e manda direto para o HTML
        hoje = date.today().isoformat()
        return render_template(
            "index.html",
            pagina="inicio",
            total_pacientes=paciente_dao.contar(),
            total_consultas=consulta_dao.contar(),
            total_agendadas=consulta_dao.contar("Agendada"),
            total_concluidas=consulta_dao.contar("Concluída"),
            proximas=consulta_dao.proximas(hoje),
        )

    @app.route("/pacientes")
    def pacientes():
        return render_template("pacientes.html", pagina="pacientes")

    @app.route("/pacientes/<int:paciente_id>")
    def ficha_paciente(paciente_id):
        paciente = paciente_dao.buscar_por_id(paciente_id)
        if paciente is None:
            abort(404)
        historico = consulta_dao.listar_por_paciente(paciente_id)
        return render_template("paciente.html", pagina="pacientes",
                               paciente=paciente, historico=historico)

    @app.route("/consultas")
    def consultas():
        return render_template("consultas.html", pagina="consultas")

    @app.route("/servicos")
    def servicos():
        return render_template("servicos.html", pagina="servicos")

    @app.route("/sobre")
    def sobre():
        return render_template("sobre.html", pagina="sobre")

    @app.route("/contato")
    def contato():
        return render_template("contato.html", pagina="contato")

    @app.errorhandler(404)
    def pagina_nao_encontrada(erro):
        return render_template("erro.html", pagina=""), 404

    @app.template_filter("data_br")
    def data_br(valor):
        """Transforma 2026-11-25 em 25/11/2026 dentro do HTML."""
        if not valor:
            return "-"
        ano, mes, dia = valor.split("-")
        return f"{dia}/{mes}/{ano}"
