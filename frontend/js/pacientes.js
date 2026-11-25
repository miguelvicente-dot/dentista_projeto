// Página de pacientes: cadastrar, listar, buscar, editar e excluir
let pacientes = [];

function mostrarTabela() {
    const busca = document.getElementById("buscaPaciente").value.toLowerCase();
    const filtrados = pacientes.filter(p => p.nome.toLowerCase().includes(busca));
    const corpo = document.getElementById("listaPacientes");
    corpo.innerHTML = filtrados.length ? filtrados.map(p => `
        <tr>
            <td><a class="link" href="/pacientes/${p.id}"><strong>${escapar(p.nome)}</strong></a></td>
            <td>${escapar(p.telefone)}</td>
            <td>${escapar(p.email || "-")}</td>
            <td>
                <a class="acao" href="/pacientes/${p.id}">Ficha</a>
                <button class="acao" onclick="prepararEdicao(${p.id})">Editar</button>
                <button class="acao excluir" onclick="apagarPaciente(${p.id})">Excluir</button>
            </td>
        </tr>`).join("") : '<tr><td colspan="4" class="vazio">Nenhum paciente encontrado.</td></tr>';
    document.getElementById("totalPacientes").textContent = pacientes.length;
}

async function carregarPacientes() {
    pacientes = await requisicao(`${API}/pacientes`);
    mostrarTabela();
}

function limparFormulario() {
    document.getElementById("formPaciente").reset();
    document.getElementById("pacienteId").value = "";
    document.getElementById("botaoSalvar").textContent = "Cadastrar paciente";
}

function prepararEdicao(id) {
    const p = pacientes.find(item => item.id === id);
    if (!p) return;
    document.getElementById("pacienteId").value = p.id;
    document.getElementById("nome").value = p.nome;
    document.getElementById("telefone").value = p.telefone;
    document.getElementById("email").value = p.email || "";
    document.getElementById("cpf").value = p.cpf || "";
    document.getElementById("data_nascimento").value = p.data_nascimento || "";
    document.getElementById("endereco").value = p.endereco || "";
    document.getElementById("botaoSalvar").textContent = "Salvar alterações";
    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function apagarPaciente(id) {
    if (!confirm("Deseja excluir este paciente? As consultas dele também serão excluídas.")) return;
    try {
        await requisicao(`${API}/pacientes/${id}`, { method: "DELETE" });
        mostrarAviso("Paciente excluído.");
        await carregarPacientes();
    } catch (erro) { mostrarAviso(erro.message); }
}

document.getElementById("formPaciente").addEventListener("submit", async evento => {
    evento.preventDefault();
    const id = document.getElementById("pacienteId").value;
    const paciente = {
        nome: document.getElementById("nome").value,
        telefone: document.getElementById("telefone").value,
        email: document.getElementById("email").value,
        cpf: document.getElementById("cpf").value,
        data_nascimento: document.getElementById("data_nascimento").value,
        endereco: document.getElementById("endereco").value
    };
    try {
        // Se tem id é edição (PUT), se não tem é cadastro novo (POST)
        await requisicao(id ? `${API}/pacientes/${id}` : `${API}/pacientes`, {
            method: id ? "PUT" : "POST",
            body: JSON.stringify(paciente)
        });
        mostrarAviso(id ? "Cadastro atualizado!" : "Paciente cadastrado!");
        limparFormulario();
        await carregarPacientes();
    } catch (erro) { mostrarAviso(erro.message); }
});

document.getElementById("cancelarEdicao").addEventListener("click", limparFormulario);
document.getElementById("buscaPaciente").addEventListener("input", mostrarTabela);

carregarPacientes().catch(erro => mostrarAviso("Erro ao carregar: " + erro.message));
