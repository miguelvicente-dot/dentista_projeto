-- Banco de dados do sistema Sorriso Fácil (SQLite)
-- O Python cria essas tabelas sozinho ao iniciar (backend/database.py).

CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT,
    cpf TEXT UNIQUE,
    data_nascimento TEXT,
    endereco TEXT
);

CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    horario TEXT NOT NULL,
    procedimento TEXT NOT NULL,
    observacoes TEXT,
    status TEXT NOT NULL DEFAULT 'Agendada',  -- Agendada, Concluída ou Cancelada
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
);

-- Dados de exemplo
INSERT INTO pacientes (nome, telefone, email, cpf, data_nascimento, endereco) VALUES
('Ana Souza', '(11) 98765-4321', 'ana@email.com', '123.456.789-00', '1995-04-12', 'Rua das Flores, 120 - Centro'),
('Bruno Lima', '(11) 91234-5678', 'bruno@email.com', '987.654.321-00', '1988-09-30', 'Av. Brasil, 455 - Jardim'),
('Carla Mendes', '(11) 99876-1234', 'carla@email.com', '456.789.123-00', '2001-01-22', 'Rua São João, 78 - Vila Nova');

INSERT INTO consultas (paciente_id, data, horario, procedimento, observacoes, status) VALUES
(1, '2026-11-15', '09:00', 'Avaliação', 'Primeira consulta', 'Concluída'),
(1, '2026-11-27', '10:30', 'Limpeza', '', 'Agendada'),
(2, '2026-11-26', '14:00', 'Restauração', 'Dente 36', 'Agendada'),
(3, '2026-11-30', '16:00', 'Avaliação', 'Sensibilidade no dente', 'Agendada');

-- Consultas úteis
-- Próximas consultas com o nome do paciente:
-- SELECT c.data, c.horario, p.nome, c.procedimento
-- FROM consultas c JOIN pacientes p ON p.id = c.paciente_id
-- WHERE c.status = 'Agendada' ORDER BY c.data, c.horario;
