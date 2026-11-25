// Funções usadas em todas as páginas
const API = "/api";

// Mostra a mensagem no canto da tela por alguns segundos
function mostrarAviso(mensagem) {
    const aviso = document.getElementById("aviso");
    aviso.textContent = mensagem;
    aviso.classList.add("mostrar");
    setTimeout(() => aviso.classList.remove("mostrar"), 2800);
}

// Faz o Fetch para o Python e já trata o erro
async function requisicao(url, opcoes = {}) {
    const resposta = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...opcoes
    });
    const dados = await resposta.json();
    if (!resposta.ok) throw new Error(dados.erro || "Ocorreu um erro.");
    return dados;
}

// Evita que um texto digitado vire código HTML na tela
function escapar(valor) {
    return String(valor ?? "").replace(/[&<>"']/g, c => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    }[c]));
}

// 2026-11-25 -> 25/11/2026
function formatarData(data) {
    if (!data) return "-";
    const [ano, mes, dia] = data.split("-");
    return `${dia}/${mes}/${ano}`;
}
