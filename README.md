# Sorriso Fácil — Clínica Odontológica

Projeto Integrado DWS + POO + Banco de Dados.

Sistema web para uma clínica odontológica: cadastro de pacientes, agenda de consultas e páginas de informação da clínica.

## Como rodar no computador
1. Instale o Python 3.
2. Abra o CMD dentro desta pasta.
3. Rode `python -m pip install -r requirements.txt`
4. Rode `python -m backend.app`
5. Abra http://127.0.0.1:5000 no navegador.

No Windows também dá para clicar duas vezes em `INICIAR_SITE.bat`.

**Não abra os arquivos de `templates/` direto no navegador.** O site só funciona com o Flask rodando.

## Publicar no Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn backend.app:app`

## Pastas
```
backend/            Python (Flask, classes, DAOs, rotas e banco)
  app.py            cria o Flask e liga tudo
  models.py         classes Paciente e Consulta (POO)
  database.py       conexão SQLite, criação das tabelas e dados de exemplo
  dao.py            PacienteDAO e ConsultaDAO (comandos SQL)
  paginas.py        rotas que devolvem as páginas HTML
  routes.py         rotas da API que devolvem JSON
frontend/
  css/style.css     visual do site
  js/comum.js       funções usadas em todas as páginas (Fetch, avisos)
  js/pacientes.js   tela de pacientes
  js/consultas.js   tela de consultas
  img/logo.svg      logo
templates/          páginas HTML (Jinja)
database/banco.sql  script SQL das tabelas
```

## Páginas
| Endereço | Página |
|---|---|
| `/` | Início com resumo e próximas consultas |
| `/pacientes` | Cadastrar, buscar, editar e excluir pacientes |
| `/pacientes/<id>` | Ficha do paciente com histórico de consultas |
| `/consultas` | Agendar, filtrar, mudar situação e excluir consultas |
| `/servicos` | Tratamentos da clínica |
| `/sobre` | História, missão e equipe |
| `/contato` | Endereço, telefones e horários |

## Rotas da API
| Método | Rota | Função |
|---|---|---|
| GET | `/api/pacientes` | Listar pacientes |
| POST | `/api/pacientes` | Cadastrar paciente |
| PUT | `/api/pacientes/<id>` | Editar paciente |
| DELETE | `/api/pacientes/<id>` | Excluir paciente |
| GET | `/api/consultas` | Listar consultas |
| POST | `/api/consultas` | Agendar consulta |
| PUT | `/api/consultas/<id>/status` | Mudar situação (Agendada, Concluída, Cancelada) |
| DELETE | `/api/consultas/<id>` | Excluir consulta |

## Banco de dados
Duas tabelas: `pacientes` e `consultas` (1 paciente tem N consultas, chave estrangeira `paciente_id`).
O arquivo `clinica.db` é criado sozinho na primeira vez que o site roda, já com 3 pacientes de exemplo.
