import sqlite3
from datetime import date, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
NOME_BANCO = ROOT_DIR / "clinica.db"

def conectar():
    """Abre uma conexão com o banco de dados."""
    conexao = sqlite3.connect(NOME_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def inicializar_banco():
    """Cria as tabelas caso elas ainda não existam."""
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT,
                cpf TEXT UNIQUE,
                data_nascimento TEXT,
                endereco TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                data TEXT NOT NULL,
                horario TEXT NOT NULL,
                procedimento TEXT NOT NULL,
                observacoes TEXT,
                status TEXT NOT NULL DEFAULT 'Agendada',
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
                    ON DELETE CASCADE
            )
        """)
    inserir_exemplos()

def inserir_exemplos():
    """Coloca alguns dados de exemplo quando o banco está vazio
    (assim o site já abre com informações para mostrar)."""
    with conectar() as conn:
        total = conn.execute("SELECT COUNT(*) FROM pacientes").fetchone()[0]
        if total > 0:
            return

        pacientes = [
            ("Ana Souza", "(11) 98765-4321", "ana@email.com", "123.456.789-00", "1995-04-12", "Rua das Flores, 120 - Centro"),
            ("Bruno Lima", "(11) 91234-5678", "bruno@email.com", "987.654.321-00", "1988-09-30", "Av. Brasil, 455 - Jardim"),
            ("Carla Mendes", "(11) 99876-1234", "carla@email.com", "456.789.123-00", "2001-01-22", "Rua São João, 78 - Vila Nova"),
        ]
        for p in pacientes:
            conn.execute("""
                INSERT INTO pacientes (nome, telefone, email, cpf, data_nascimento, endereco)
                VALUES (?, ?, ?, ?, ?, ?)
            """, p)

        hoje = date.today()
        consultas = [
            (1, hoje - timedelta(days=10), "09:00", "Avaliação", "Primeira consulta", "Concluída"),
            (1, hoje + timedelta(days=2), "10:30", "Limpeza", "", "Agendada"),
            (2, hoje + timedelta(days=1), "14:00", "Restauração", "Dente 36", "Agendada"),
            (3, hoje + timedelta(days=5), "16:00", "Avaliação", "Sensibilidade no dente", "Agendada"),
        ]
        for c in consultas:
            conn.execute("""
                INSERT INTO consultas (paciente_id, data, horario, procedimento, observacoes, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (c[0], c[1].isoformat(), c[2], c[3], c[4], c[5]))
