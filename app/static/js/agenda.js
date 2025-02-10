import {
    buscarNomeIdPaciente,
    buscarNomeIdTutor,
    buscarNomeStatus,
    buscarPacientesPorTutor,
    buscarTutorCpf
} from "./buscas.js";

document.addEventListener("DOMContentLoaded", function () {
    // Constantes dos elementos da página de agenda
    const dataInput = document.getElementById("dataSelecionada");
    const listaAgendamentos = document.getElementById("listaAgendamentos");
    const dataAtualSpan = document.getElementById("dataAtual");
    const agendaDiv = document.getElementById("agenda");
    const agendaControls = document.getElementById("agenda-controls");
    const novoAgendamentoBtn = document.getElementById("novoAgendamento");

    // Configurar evento do botão "Carregar Tutor"
    configurarCarregarTutorBtn();

    // Função para atualizar a agenda conforme a data escolhida
    let agendamentosData = [];
    try {
        agendamentosData = JSON.parse(document.getElementById("agendamentos-data").textContent);
    } catch (error) {
        console.error("Erro ao carregar agendamentos:", error);
        agendamentosData = [];
    }

    async function atualizarAgenda(dataSelecionada) {
        listaAgendamentos.innerHTML = ""; // Limpa a tabela antes de adicionar os novos dados
        const dataFormatada = new Date(dataSelecionada).toISOString().split("T")[0];

        const agendamentosFiltrados = agendamentosData
            .filter(agendamento => agendamento.data === dataFormatada)
            .sort((a, b) => a.hora.localeCompare(b.hora));

        dataAtualSpan.textContent = dataSelecionada ? formatarData(dataSelecionada) : "Selecione um dia";
        agendaDiv.style.display = "block";

        if (agendaControls) {
            agendaControls.style.display = "block";
        }

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
                    </td>
                `;
                listaAgendamentos.appendChild(row);
            }
        } else {
            listaAgendamentos.innerHTML = `<tr><td colspan="4" style="text-align:center;">Nenhum agendamento encontrado para este dia.</td></tr>`;
        }
    }

    dataInput.addEventListener("change", function () {
        atualizarAgenda(this.value).then(() => console.log("Agenda atualizada!"));
    });

    if (dataInput.value) {
        atualizarAgenda(dataInput.value).then(() => console.log("Agenda inicializada!"));
    }

    if (novoAgendamentoBtn) {
        novoAgendamentoBtn.addEventListener("click", function () {
            const dataSelecionada = dataInput.value;
            if (!dataSelecionada) {
                alert("Por favor, selecione uma data antes de agendar.");
                return;
            }
            abrirPopupCadastro(dataSelecionada);
        });
    }
});

// ==================
// Função separada para configurar o evento do botão "Carregar Tutor"
// ==================
function configurarCarregarTutorBtn() {
    const carregarTutorBtn = document.getElementById("carregarTutor");
    if (!carregarTutorBtn) {
        console.error("Botão 'Carregar Tutor' não encontrado no DOM!");
        return;
    }

    document.addEventListener("click", function (event) {
    if (event.target && event.target.id === "carregarTutor") {
        document.getElementById("loadingTutor").style.display = "inline"; // Mostra "Carregando..."
        atualizarListaPacientes().then(() => {
            document.getElementById("loadingTutor").style.display = "none"; // Esconde após carregar
        });
    }
});

}

// ==================
// Função separada para buscar pacientes por tutor
// ==================
async function atualizarListaPacientes() {
    const tutorInput = document.getElementById("tutor");
    const pacienteSelect = document.getElementById("paciente");

    let cpfTutor = tutorInput.value.trim();
    cpfTutor = formatarCPF(cpfTutor);

    const mensagemTutor = document.getElementById("mensagemTutor");

    if (!cpfTutor) {
        pacienteSelect.innerHTML = "<option value=''>Informe um tutor.</option>";
        mensagemTutor.style.display = "none";
        return;
    }

    try {
        const tutor = await buscarTutorCpf(cpfTutor);
        if (!tutor || !tutor.id) {
            alert("Faça o cadastro do tutor antes de cadastrar um paciente.");
            pacienteSelect.innerHTML = "<option value=''>Nenhum paciente disponível.</option>";
            mensagemTutor.style.display = "block";
            return;
        }

        mensagemTutor.style.display = "none";
        const pacientes = await buscarPacientesPorTutor(tutor.id);
        pacienteSelect.innerHTML = "<option value=''>Selecione um paciente</option>";

        if (pacientes.length === 0) {
            alert("Nenhum paciente cadastrado para este tutor.");
            pacienteSelect.innerHTML = "<option value=''>Nenhum paciente disponível.</option>";
        } else {
            pacientes.forEach(paciente => {
                const option = document.createElement("option");
                option.value = paciente.id;
                option.textContent = paciente.nome;
                pacienteSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error("Erro ao buscar tutor:", error);
        alert("Erro ao buscar tutor.");
    }
}

// ==================
// Funções auxiliares
// ==================
function formatarCPF(cpf) {
    cpf = cpf.replace(/\D/g, "");
    if (cpf.length === 11) {
        return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
    }
    return cpf;
}

export async function editarAgendamento(id) {
    try {
        // Buscar os dados do agendamento selecionado
        const response = await fetch("/api/agendamentos");
        const agendamentos = await response.json();
        const agendamento = agendamentos.find(a => a.id === parseInt(id));

        if (!agendamento) {
            console.error("Agendamento não encontrado!");
            return;
        }

        // Buscar HTML do popup de edição
        const htmlResponse = await fetch("/editar_agendamento");
        // Inserir o HTML carregado dentro do container correto
        document.getElementById("popupContainer").innerHTML = await htmlResponse.text();

        // Garantir que os elementos foram carregados corretamente
        const dataElement = document.getElementById("data");
        const tutorElement = document.getElementById("tutor");
        const pacienteElement = document.getElementById("paciente");
        const horarioElement = document.getElementById("horario");
        const statusElement = document.getElementById("status");

        if (!dataElement || !tutorElement || !pacienteElement || !horarioElement || !statusElement) {
            console.error("Elementos do popup de edição não encontrados!");
            return;
        }

        // Formatar e preencher os dados
        const dataFormatada = formatarData(agendamento.data);
        const nomeTutor = await buscarNomeIdTutor(agendamento.tutor);
        const nomePaciente = await buscarNomeIdPaciente(agendamento.paciente);

        dataElement.value = dataFormatada;
        tutorElement.value = nomeTutor;
        pacienteElement.value = nomePaciente;
        horarioElement.value = agendamento.hora;

        // Buscar e preencher a lista de status
        const statusResponse = await fetch("/api/status");
        const statusList = await statusResponse.json();

        statusElement.innerHTML = "";
        statusList.forEach(status => {
            let option = document.createElement("option");
            option.value = status.id;
            option.textContent = status.nome;
            statusElement.appendChild(option);
        });

        // Definir o status selecionado
        statusElement.value = agendamento.status;

        // Exibir a popup de edição
        document.getElementById("editar-popup").style.display = "flex";

    } catch (error) {
        console.error("Erro ao abrir popup de edição:", error);
    }
}


function abrirPopupCadastro(dataSelecionada) {
    fetch("/cadastro_agendamento")
        .then(response => response.text())
        .then(html => {
            // document.getElementById("popupContainer").innerHTML = html;
            document.getElementById("cadastro-popup").style.display = "flex";

            document.getElementById("dataSelecionadaPopup").textContent = formatarData(dataSelecionada);
            document.getElementById("data").value = dataSelecionada;
        })
        .catch(error => console.error("Erro ao carregar popup: ", error));
}

function fecharPopupCadastro() {
    document.getElementById("cadastro-popup").style.display = "none";
}

function fecharPopupEdicao() {
    document.getElementById("editar-popup").style.display = "none";
}

function enviarFormulario() {
    const form = document.getElementById("cadastroForm");
    const formData = new FormData(form);

    fetch("/cadastro_agendamento", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensagem);
        fecharPopupCadastro();
    })
    .catch(error => console.error("Erro ao enviar formulário: ", error));
}

function formatarData(data) {
    return data.split("-").reverse().join("/");
}



window.abrirPopupCadastro = abrirPopupCadastro;
window.fecharPopupCadastro = fecharPopupCadastro;
window.editarAgendamento = editarAgendamento;
window.fecharPopupEdicao = fecharPopupEdicao;