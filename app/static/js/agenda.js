import { buscarNomeIdPaciente, buscarNomeIdTutor, buscarNomeStatus } from "./buscas.js";

document.addEventListener("DOMContentLoaded", function () {
    const dataInput = document.getElementById("dataSelecionada");
    const listaAgendamentos = document.getElementById("listaAgendamentos");
    const dataAtualSpan = document.getElementById("dataAtual");
    const agendaDiv = document.getElementById("agenda");

    // Obter os agendamentos do JSON embutido na página
    let agendamentosData = [];

    // Tenta carregar os dados do JSON embutido na página
    try {
        agendamentosData = JSON.parse(document.getElementById("agendamentos-data").textContent);
    } catch (error) {
        console.error("Erro ao carregar os agendamentos:", error);
        agendamentosData = []; // Garante que não seja null caso ocorra erro
    }

    // Exibe a agenda antes de preencher os dados (CORREÇÃO AQUI)
    //agendaDiv.classList.add("active");

    // Função para atualizar a agenda conforme a data escolhida
    async function atualizarAgenda(dataSelecionada) {
        listaAgendamentos.innerHTML = ""; // Limpa a tabela antes de adicionar os novos dados

        // Formatar a data para o formato YYYY-MM-DD
        const dataFormatada = new Date(dataSelecionada).toISOString().split("T")[0];

        // Filtrar os agendamentos para a data selecionada e ordenar por horário
        const agendamentosFiltrados = agendamentosData
            .filter(agendamento => agendamento.data === dataFormatada)
            .sort((a, b) => a.hora.localeCompare(b.hora)); // Ordenar por horário

        // Atualiza o título da seção
        dataAtualSpan.textContent = dataSelecionada ? dataSelecionada.split("-").reverse().join("/") : "Selecione um dia";

        agendaDiv.style.display = "block";
        // Se houver agendamentos, exibe a tabela e preenche os dados
        if (agendamentosFiltrados.length > 0) {
            for (const agendamento of agendamentosFiltrados) {
                const row = document.createElement("tr");

                const nomePaciente = await buscarNomeIdPaciente(agendamento.paciente);
                const nomeTutor = await buscarNomeIdTutor(agendamento.tutor);
                const nomeStatus = await buscarNomeStatus(agendamento.status);

                row.innerHTML = `
                    <td>${agendamento.hora}</td>
                    <td>${nomePaciente || "Não informado"} (${nomeTutor || "Sem tutor"})</td>
                    <td>${nomeStatus}</td>
                    <td>
                        <button class="editar" onclick="editarAgendamento(${agendamento.id})">Editar</button>
                        <button class="excluir" onclick="excluirAgendamento(${agendamento.id})">Excluir</button>
                    </td>
                `;
                listaAgendamentos.appendChild(row);
            }
        } else {
            listaAgendamentos.innerHTML = `<tr><td colspan="4" style="text-align:center;">Nenhum agendamento encontrada para este dia.</td></tr>`;
            //agendaDiv.style.display = "block"; // Mantém a tabela visível mesmo se vazia
        }
    }

    // Evento para atualizar a agenda quando o usuário escolher uma data
    dataInput.addEventListener("change", function () {
        atualizarAgenda(this.value).then(r => console.log("Agenda atualizada!"));
    });

    // Inicializa a agenda se houver uma data pré-selecionada
    if (dataInput.value) {
        atualizarAgenda(dataInput.value).then(r => console.log("Agenda inicializada!"));
    }
});


function editarAgendamento(id) {
    console.log("Editar agendamento com ID:", id);
}

function excluirAgendamento(id) {
    console.log("Excluir agendamento com ID:", id);
}