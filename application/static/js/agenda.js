document.addEventListener("DOMContentLoaded", function () {
    const botaoSalvar = document.getElementById("salvarEdicao");

    if (botaoSalvar) {
        botaoSalvar.addEventListener("click", enviarEdicao);
    }

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
                    <td>${agendamento.status}</td>
                    <td>${agendamento.veterinario}</td>
                    
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

async function editarAgendamento(id_agendamento) {
    try {
        let popupContainer = document.getElementById("editar-popup");

        if (!popupContainer) {
            const responsePopup = await fetch("/editar_agendamento_page");
            const htmlPopup = await responsePopup.text();

            const div = document.createElement("div");
            div.innerHTML = htmlPopup;
            document.body.appendChild(div);

            popupContainer = document.getElementById("editar-popup");

            // Adiciona o evento ao botão "Salvar" após carregar o popup
            const botaoSalvar = document.getElementById("salvarEdicao");
            if (botaoSalvar) {
                botaoSalvar.addEventListener("click", enviarEdicao);
            }
        }

        const response = await fetch(`/api/agendamentos/${id_agendamento}`);
        const agendamento = await response.json();

        if (!response.ok) {
            alert("Erro ao carregar agendamento: " + agendamento.erro);
            return;
        }

        console.log("Agendamento encontrado:", agendamento);

        document.getElementById("id_agendamento").value = agendamento["id_agendamento"];
        await carregarStatus(agendamento["id_status"]);

        popupContainer.style.display = "flex";

    } catch (error) {
        console.error("Erro ao carregar dados do agendamento:", error);
        alert("Erro ao carregar agendamento.");
    }
}



async function carregarStatus(id_status_selecionado) {
    try {
        const response = await fetch("/api/status");
        const statusLista = await response.json();

        if (!response.ok) {
            alert("Erro ao carregar status.");
            return;
        }

        const selectStatus = document.getElementById("status");
        selectStatus.innerHTML = '<option value="">Selecione um status</option>';

        statusLista.forEach(status => {
            let option = document.createElement("option");
            option.value = status.id;
            option.textContent = status.nome;
            if (status.id === id_status_selecionado) {
                option.selected = true;
            }
            selectStatus.appendChild(option);
        });

    } catch (error) {
        console.error("Erro ao carregar status:", error);
        alert("Erro ao carregar status.");
    }
}

async function enviarEdicao() {
    const id_agendamento = document.getElementById("id_agendamento").value;
    const status = document.getElementById("status").value;

    if (!id_agendamento || !status) {
        alert("Selecione um status para atualizar.");
        return;
    }

    const dadosEdicao = { status };

    try {
        const response = await fetch(`/api/agendamentos/${id_agendamento}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dadosEdicao)
        });

        const resposta = await response.json();

        if (response.ok) {
            alert("Status atualizado com sucesso!");
            fecharPopupEdicao();
            await atualizarAgenda(document.getElementById("dataSelecionada").value);
        } else {
            alert("Erro ao atualizar status: " + resposta.erro);
        }
    } catch (error) {
        console.error("Erro ao atualizar agendamento:", error);
        alert("Erro ao atualizar status.");
    }
}



function fecharPopupEdicao() {
    document.getElementById("editar-popup").style.display = "none";
}

// Expor funções globalmente
window.editarAgendamento = editarAgendamento;
window.enviarEdicao = enviarEdicao;
window.fecharPopupEdicao = fecharPopupEdicao;


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
    const id_animal = document.getElementById("paciente").value;
    const id_veterinario = document.getElementById("veterinario").value;
    const data = document.getElementById("data").value;
    const horario = document.getElementById("horario").value;
    const id_especialidade = document.getElementById("especialidade").value;

    console.log("Dados capturados antes do envio:", {
        id_animal,
        id_veterinario,
        data,
        horario,
        id_especialidade
    });

    if (!id_animal || !id_veterinario || !horario || !id_especialidade) {
        alert("Todos os campos são obrigatórios. Verifique se preencheu corretamente.");
        return;
    }

    const dadosAgendamento = {
        id_animal,
        id_veterinario,
        data,
        horario,
        id_especialidade
    };

    try {
        const response = await fetch("/cadastro_agendamento", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dadosAgendamento)
        });

        const dataResponse = await response.json();

        if (response.ok) {
            alert("Agendamento cadastrado com sucesso!");
            fecharPopupCadastro();
            await atualizarAgenda(document.getElementById("dataSelecionada").value);
        } else {
            alert(`Erro: ${dataResponse.erro}`);
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

    if (!especialidade) {
        selectVet.innerHTML = '<option value="">Selecione uma especialidade primeiro</option>';
        return;
    }

    try {
        const response = await fetch(`/api/veterinarios_disponiveis?especialidade_id=${especialidade}`);
        const veterinarios = await response.json();

        selectVet.innerHTML = veterinarios.length
            ? '<option value="">Selecione um veterinário</option>'
            : '<option value="">Nenhum veterinário disponível</option>';

        veterinarios.forEach(vet => {
            let option = document.createElement("option");
            option.value = vet["id"];
            option.textContent = vet["nome"];
            selectVet.appendChild(option);
        });

        console.log("Veterinários carregados:", veterinarios);

        // Chamar a função para carregar horários
        await carregarHorarios();

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
        const response = await fetch("/api/horarios");
        const horarios = await response.json();

        selectHorario.innerHTML = horarios.length
            ? '<option value="">Selecione um horário</option>'
            : '<option value="">Nenhum horário disponível</option>';

        horarios.forEach(horario => {
            let option = document.createElement("option");
            option.value = horario;
            option.textContent = horario;
            selectHorario.appendChild(option);
        });

        console.log("Horários carregados:", horarios);

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
