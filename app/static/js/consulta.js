document.addEventListener("DOMContentLoaded", function () {
    // Certifique-se de que esses elementos existem antes de usá-los
    const dataInput = document.getElementById("dataSelecionada");
    const listaAgendamentos = document.getElementById("listaAgendamentos");
    const dataAtualSpan = document.getElementById("dataAtual"); // Corrigido
    const agendaDiv = document.getElementById("agenda"); // Corrigido
    const novoAgendamentoBtn = document.getElementById("novoAgendamento");

    dataInput.addEventListener("change", function () {
        atualizarAgenda(this.value);
    });

    if (dataInput.value) {
        atualizarAgenda(dataInput.value);
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

// ====================
// Função para Atualizar Agenda
// ====================
async function atualizarAgenda(dataSelecionada) {
    // Verificar se os elementos existem antes de usá-los
    const dataAtualSpan = document.getElementById("dataAtual");
    const agendaDiv = document.getElementById("agenda");
    const listaAgendamentos = document.getElementById("listaAgendamentos");

    if (!dataAtualSpan || !agendaDiv || !listaAgendamentos) {
        console.error("Erro: Elementos da agenda não foram encontrados.");
        return;
    }

    listaAgendamentos.innerHTML = "";

    if (!dataSelecionada) {
        dataAtualSpan.textContent = "Selecione um dia";
        agendaDiv.style.display = "none";
        return;
    }

    try {
        const response = await fetch(`/api/agendamentos?data=${dataSelecionada}`);
        const agendamentosData = await response.json();

        if (response.status !== 200) {
            throw new Error(agendamentosData.erro || "Erro desconhecido ao carregar agendamentos.");
        }

        dataAtualSpan.textContent = formatarData(dataSelecionada);
        agendaDiv.style.display = "block";

        if (agendamentosData.length > 0) {
            for (const agendamento of agendamentosData) {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${agendamento.horario}</td>
                    <td>${agendamento.paciente} (${agendamento.tutor})</td>
                    <td>${agendamento.veterinario}</td>
                    <td>${agendamento.status}</td>
                    <td>
                        <button class="editar" onclick="editarAgendamento(${agendamento.id_agendamento})">Editar</button>
                    </td>
                `;

                listaAgendamentos.appendChild(row);
            }
        } else {
            listaAgendamentos.innerHTML = `<tr><td colspan="5" style="text-align:center;">Nenhum agendamento encontrado para este dia.</td></tr>`;
        }
    } catch (error) {
        console.error("Erro ao carregar agendamentos:", error);
        listaAgendamentos.innerHTML = `<tr><td colspan="5" style="text-align:center; color: red;">Erro ao carregar agendamentos.</td></tr>`;
        agendaDiv.style.display = "block";
    }
}

// ====================
// Funções para Cadastro de Agendamento
// ====================
async function abrirPopupCadastro(dataSelecionada) {
    try {
        const response = await fetch("/cadastro_agendamento_page");
        const html = await response.text();

            document.getElementById("popupContainer").innerHTML = html;
            document.getElementById("cadastro-popup").style.display = "flex";

            // Define a data no formulário
            document.getElementById("dataSelecionadaPopup").textContent = formatarData(dataSelecionada);
            document.getElementById("data").value = dataSelecionada;

            await carregarEspecialidades();

            await carregarHorarios();// Adiciona um pequeno atraso para evitar sobreposição

        } catch (error) {
    console.error("Erro ao carregar popup: ", error);
    }
}

function fecharPopupCadastro() {
    document.getElementById("cadastro-popup").style.display = "none";
}

// ====================
// Função para Enviar Formulário de Agendamento
// ====================
document.addEventListener("submit", function (event) {
    if (event.target.id === "cadastroForm") {
        event.preventDefault();
        enviarFormulario();
    }
});

async function enviarFormulario() {
    const form = document.getElementById("cadastroForm");
    const formData = new FormData(form);

    try {
        const response = await fetch("/cadastro_agendamento", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            alert("Agendamento cadastrado com sucesso!");
            fecharPopupCadastro();
            atualizarAgenda(document.getElementById("dataSelecionada").value);
        } else {
            alert(`Erro: ${data.erro}`);
        }
    } catch (error) {
        console.error("Erro ao enviar formulário: ", error);
        alert("Erro ao cadastrar agendamento.");
    }
}

// ====================
// Funções Auxiliares
// ====================
function formatarData(data) {
    if (!data) return "";
    return data.split("-").reverse().join("/");
}

async function atualizarListaPacientes() {
    const tutorInput = document.getElementById("tutor");
    const pacienteSelect = document.getElementById("paciente");
    const loadingTutor = document.getElementById("loadingTutor");

    let cpfTutor = tutorInput.value.trim();

    if (!cpfTutor) {
        pacienteSelect.innerHTML = "<option value=''>Informe um tutor.</option>";
        return;
    }

    // Exibe "Carregando..."
    loadingTutor.style.display = "inline";

    try {
        // Buscar os pacientes pelo CPF do tutor
        const response = await fetch(`/api/pacientes_por_tutor?cpf=${cpfTutor}`);

        if (!response.ok) {
            throw new Error("Erro ao buscar pacientes do tutor.");
        }

        const pacientes = await response.json();

        // Verificar se há erro na resposta
        if (pacientes.erro) {
            alert(pacientes.erro);
            pacienteSelect.innerHTML = "<option value=''>Nenhum paciente disponível.</option>";
            return;
        }

        // Preencher a lista de pacientes
        pacienteSelect.innerHTML = "<option value=''>Selecione um paciente</option>";

        if (pacientes.length === 0) {
            alert("Nenhum paciente cadastrado para este tutor.");
            pacienteSelect.innerHTML = "<option value=''>Nenhum paciente disponível.</option>";
        } else {
            pacientes.forEach(paciente => {
                let option = document.createElement("option");
                option.value = paciente["id"];
                option.textContent = paciente["nome"];
                pacienteSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error("Erro ao buscar pacientes:", error);
        alert("Erro ao carregar os pacientes do tutor.");
    } finally {
        // Esconde "Carregando..."
        loadingTutor.style.display = "none";
    }
}

async function carregarVeterinarios() {
    const especialidade = document.getElementById("especialidade").value;
    const selectVet = document.getElementById("veterinario");

    // Verifica se a especialidade foi selecionada
    if (!especialidade) {
        selectVet.innerHTML = '<option value="">Selecione uma especialidade primeiro</option>';
        return;
    }

    try {
        let url = `/api/veterinarios_disponiveis?especialidade_id=${especialidade}`;

        const response = await fetch(url);
        const veterinarios = await response.json();

        if (!veterinarios || veterinarios.length === 0) {
            selectVet.innerHTML = '<option value="">Nenhum veterinário disponível.</option>';
            return;
        }

        selectVet.innerHTML = '<option value="">Selecione um veterinário</option>';

        console.log("vet:", veterinarios);

        if (!veterinarios || veterinarios.length === 0) {
            selectVet.innerHTML = '<option value="">Nenhum veterinário disponível.</option>';
            return;
        }

        veterinarios.forEach(vet => {
            let option = document.createElement("option");
            option.value = vet.id;
            option.textContent = vet.nome;
            selectVet.appendChild(option);
        });
    } catch (error) {
        console.error("Erro ao carregar veterinários:", error);
        alert("Erro ao carregar veterinários.");
    }
}

async function carregarHorarios() {
    const selectHorario = document.getElementById("horario");

    if (!selectHorario) {
        console.error("Elemento select de horários não encontrado.");
        return;
    }

    selectHorario.innerHTML = '<option value="">Carregando horários...</option>';

    try {
        let url = "/api/horarios";

        const response = await fetch(url);
        const horarios = await response.json();

        console.log("Horários recebidos (antes de verificar tipo):", horarios);

        selectHorario.innerHTML = '<option value="">Selecione um horário</option>';

        if (horarios.length === 0) {
            selectHorario.innerHTML = '<option value="">Nenhum horário disponível</option>';
            return;
        }

        horarios.forEach(horario => {
            let option = document.createElement("option");
            option.value = horario;
            option.textContent = horario;
            selectHorario.appendChild(option);
        });
        console.log("Lista de horários final:", horarios);

    } catch (error) {
        console.error("Erro ao carregar horários:", error);
        alert("Erro ao carregar horários.");
    }
}

async function carregarEspecialidades() {
    const selectEspecialidade = document.getElementById("especialidade");

    if (!selectEspecialidade) {
        console.error("Elemento select de especialidades não encontrado.");
        return;
    }

    try {
        const response = await fetch("/api/especialidades");
        const especialidades = await response.json();

        // Verifica se especialidades é uma lista válida
        if (!Array.isArray(especialidades)) {
            throw new Error("Resposta da API não é um array válido.");
        }

        selectEspecialidade.innerHTML = '<option value="">Selecione uma especialidade</option>';

        console.log("especialidades:", especialidades);

        especialidades.forEach(especialidade => {
            console.log(especialidade);
            let option = document.createElement("option");
            option.value = especialidade["id"];
            option.textContent = especialidade["nome"];
            selectEspecialidade.appendChild(option);
        });
        console.log("Lista final de especialidades:", especialidades);
    } catch (error) {
        console.error("Erro ao carregar especialidades:", error);
        alert("Erro ao carregar especialidades.");
    }
}



// ====================
// Expor funções globalmente
// ====================
window.abrirPopupCadastro = abrirPopupCadastro;
window.fecharPopupCadastro = fecharPopupCadastro;
window.atualizarListaPacientes = atualizarListaPacientes;
window.carregarVeterinarios = carregarVeterinarios;
window.carregarHorarios = carregarHorarios;
window.carregarEspecialidades = carregarEspecialidades;
