// Página de consultas: agendar, listar, filtrar, mudar situação e excluir
let consultas = [];

async function carregarPacientesNoSelect() {
    const pacientes = await requisicao(`${API}/pacientes`);
    const select = document.getElementById("consultaPaciente");
    select.innerHTML = '<option value="">Selecione um paciente</option>' +
        pacientes.map(p => `<option value="${p.id}">${escapar(p.nome)}</option>`).join("");
}

function mostrarTabela() {
    const filtro = document.getElementById("filtroStatus").value;
    const filtradas = consultas.filter(c => !filtro || c.status === filtro);
    const corpo = document.getElementById("listaConsultas");
    corpo.innerHTML = filtradas.length ? filtradas.map(c => `
        <tr>
            <td><a class="link" href="/pacientes/${c.paciente_id}">${escapar(c.paciente_nome)}</a></td>
            <td>${formatarData(c.data)}</td>
            <td>${escapar(c.horario)}</td>
            <td>${escapar(c.procedimento)}</td>
            <td>
                <select class="mudar-status status-${c.status.toLowerCase()}" onchange="mudarStatus(${c.id}, this.value)">
                    ${["Agendada", "Concluída", "Cancelada"].map(s =>
                        `<option ${s === c.status ? "selected" : ""}>${s}</option>`).join("")}
                </select>
            </td>
            <td><button class="acao excluir" onclick="apagarConsulta(${c.id})">Excluir</button></td>
        </tr>`).join("") : '<tr><td colspan="6" class="vazio">Nenhuma consulta encontrada.</td></tr>';
    document.getElementById("totalConsultas").textContent = consultas.length;
}

async function carregarConsultas() {
    consultas = await requisicao(`${API}/consultas`);
    mostrarTabela();
}

async function mudarStatus(id, status) {
    try {
        const resposta = await requisicao(`${API}/consultas/${id}/status`, {
            method: "PUT",
            body: JSON.stringify({ status })
        });
        mostrarAviso(resposta.mensagem);
        await carregarConsultas();
    } catch (erro) { mostrarAviso(erro.message); }
}

async function apagarConsulta(id) {
    if (!confirm("Deseja excluir esta consulta?")) return;
    try {
        await requisicao(`${API}/consultas/${id}`, { method: "DELETE" });
        mostrarAviso("Consulta excluída.");
        await carregarConsultas();
    } catch (erro) { mostrarAviso(erro.message); }
}

document.getElementById("formConsulta").addEventListener("submit", async evento => {
    evento.preventDefault();
    const consulta = {
        paciente_id: document.getElementById("consultaPaciente").value,
        data: document.getElementById("consultaData").value,
        horario: document.getElementById("consultaHorario").value,
        procedimento: document.getElementById("procedimento").value,
        observacoes: document.getElementById("observacoes").value
    };
    try {
        await requisicao(`${API}/consultas`, { method: "POST", body: JSON.stringify(consulta) });
        mostrarAviso("Consulta agendada!");
        evento.target.reset();
        await carregarConsultas();
    } catch (erro) { mostrarAviso(erro.message); }
});

document.getElementById("filtroStatus").addEventListener("change", mostrarTabela);

Promise.all([carregarPacientesNoSelect(), carregarConsultas()])
    .catch(erro => mostrarAviso("Erro ao carregar: " + erro.message));
