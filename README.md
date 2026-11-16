# Sorriso Fácil — Clínica Odontológica

Projeto Integrado DWS + POO + Banco de Dados.

## Executar no computador
1. Instale Python 3.
2. Abra esta pasta no VS Code.
3. Execute `pip install -r requirements.txt`.
4. Execute `python -m backend.app`.
5. Acesse http://127.0.0.1:5000.

No Windows, também pode usar `INICIAR_SITE.bat`.

**Não abra `templates/index.html` diretamente.** Inicie o Flask e acesse pelo endereço acima.

## Publicar no Render
- Root Directory: vazio.
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn backend.app:app`

A pasta `backend` deve estar na raiz do repositório, junto de `requirements.txt`.

## Pastas
- `backend/`: Python, Flask, classes, DAOs, rotas e banco.
- `frontend/css/`: CSS.
- `frontend/js/`: JavaScript e Fetch.
- `templates/`: HTML.
- `database/`: script SQL.
- `clinica.db`: banco SQLite criado automaticamente.

## Funcionalidades
- Cadastrar, listar, editar e excluir pacientes.
- Pesquisar pacientes pelo nome.
- Agendar, listar e excluir consultas.
- Exibir totais de pacientes e consultas.

## Rotas
| Método | Rota | Função |
|---|---|---|
| GET | `/api/pacientes` | Listar pacientes |
| POST | `/api/pacientes` | Cadastrar paciente |
| PUT | `/api/pacientes/<id>` | Editar paciente |
| DELETE | `/api/pacientes/<id>` | Excluir paciente |
| GET | `/api/consultas` | Listar consultas |
| POST | `/api/consultas` | Agendar consulta |
| DELETE | `/api/consultas/<id>` | Excluir consulta |

## Explicação para apresentação
"Meu projeto é um sistema para uma clínica odontológica. O HTML monta a página, o CSS cuida do visual e o JavaScript usa Fetch para conversar com o Python. O Flask recebe as solicitações pelas rotas. Usei as classes Paciente e Consulta para representar os dados, e os DAOs organizam os comandos que acessam o banco SQLite."
