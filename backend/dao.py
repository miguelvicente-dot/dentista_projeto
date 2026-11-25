from .database import conectar
from .models import Paciente, Consulta

class PacienteDAO:
    """DAO: concentra os comandos SQL relacionados aos pacientes."""

    def cadastrar(self, paciente):
        with conectar() as conn:
            cursor = conn.execute("""
                INSERT INTO pacientes (nome, telefone, email, cpf, data_nascimento, endereco)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (paciente.nome, paciente.telefone, paciente.email, paciente.cpf,
                  paciente.data_nascimento, paciente.endereco))
            paciente.id = cursor.lastrowid
        return paciente

    def listar(self):
        with conectar() as conn:
            linhas = conn.execute("SELECT * FROM pacientes ORDER BY nome").fetchall()
        return [Paciente(l["nome"], l["telefone"], l["email"] or "", l["cpf"] or "",
                         l["data_nascimento"] or "", l["endereco"] or "", l["id"])
                for l in linhas]

    def buscar_por_id(self, paciente_id):
        with conectar() as conn:
            l = conn.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_id,)).fetchone()
        if not l:
            return None
        return Paciente(l["nome"], l["telefone"], l["email"] or "", l["cpf"] or "",
                        l["data_nascimento"] or "", l["endereco"] or "", l["id"])

    def atualizar(self, paciente_id, paciente):
        with conectar() as conn:
            cursor = conn.execute("""
                UPDATE pacientes
                SET nome=?, telefone=?, email=?, cpf=?, data_nascimento=?, endereco=?
                WHERE id=?
            """, (paciente.nome, paciente.telefone, paciente.email, paciente.cpf,
                  paciente.data_nascimento, paciente.endereco, paciente_id))
        return cursor.rowcount > 0

    def excluir(self, paciente_id):
        with conectar() as conn:
            cursor = conn.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
        return cursor.rowcount > 0

    def contar(self):
        with conectar() as conn:
            return conn.execute("SELECT COUNT(*) FROM pacientes").fetchone()[0]


class ConsultaDAO:
    """DAO: concentra os comandos SQL relacionados às consultas."""

    def cadastrar(self, consulta):
        with conectar() as conn:
            cursor = conn.execute("""
                INSERT INTO consultas (paciente_id, data, horario, procedimento, observacoes, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (consulta.paciente_id, consulta.data, consulta.horario,
                  consulta.procedimento, consulta.observacoes, consulta.status))
            consulta.id = cursor.lastrowid
        return consulta

    def listar(self):
        with conectar() as conn:
            linhas = conn.execute("""
                SELECT c.*, p.nome AS paciente_nome
                FROM consultas c
                JOIN pacientes p ON p.id = c.paciente_id
                ORDER BY c.data, c.horario
            """).fetchall()
        return [dict(linha) for linha in linhas]

    def listar_por_paciente(self, paciente_id):
        """Histórico de consultas de um paciente (usado na ficha)."""
        with conectar() as conn:
            linhas = conn.execute("""
                SELECT * FROM consultas
                WHERE paciente_id = ?
                ORDER BY data DESC, horario DESC
            """, (paciente_id,)).fetchall()
        return [dict(linha) for linha in linhas]

    def proximas(self, hoje, limite=5):
        """Próximas consultas agendadas a partir de hoje (usado na página inicial)."""
        with conectar() as conn:
            linhas = conn.execute("""
                SELECT c.*, p.nome AS paciente_nome
                FROM consultas c
                JOIN pacientes p ON p.id = c.paciente_id
                WHERE c.data >= ? AND c.status = 'Agendada'
                ORDER BY c.data, c.horario
                LIMIT ?
            """, (hoje, limite)).fetchall()
        return [dict(linha) for linha in linhas]

    def contar(self, status=None):
        with conectar() as conn:
            if status:
                return conn.execute("SELECT COUNT(*) FROM consultas WHERE status = ?", (status,)).fetchone()[0]
            return conn.execute("SELECT COUNT(*) FROM consultas").fetchone()[0]

    def atualizar_status(self, consulta_id, status):
        with conectar() as conn:
            cursor = conn.execute("UPDATE consultas SET status = ? WHERE id = ?", (status, consulta_id))
        return cursor.rowcount > 0

    def excluir(self, consulta_id):
        with conectar() as conn:
            cursor = conn.execute("DELETE FROM consultas WHERE id = ?", (consulta_id,))
        return cursor.rowcount > 0
