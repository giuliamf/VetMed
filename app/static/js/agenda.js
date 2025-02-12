document.addEventListener("DOMContentLoaded", function () {
    const listaAgendamentos = document.getElementById("listaAgendamentos");
    const dataAtualSpan = document.getElementById("dataAtual");
    const dataInput = document.getElementById("dataSelecionada");
    const agendaDiv = document.getElementById("agenda"); // Seleciona a div da agenda

    async function carregarAgendamentos(dataSelecionada) {
        listaAgendamentos.innerHTML = ""; // Limpa os agendamentos anteriores

        if (!dataSelecionada) {
            dataAtualSpan.textContent = "Selecione um dia";
            agendaDiv.style.display = "none"; // Garante que a agenda fique oculta se nenhuma data for selecionada
            return;
        }

        try {
            // Faz a requisição para a API Flask
            const response = await fetch("/api/agendamentos");
            const agendamentosData = await response.json();

            // Filtra os agendamentos pela data escolhida
            const dataFormatada = new Date(dataSelecionada).toISOString().split("T")[0];
            const agendamentosFiltrados = agendamentosData
                .filter(agendamento => agendamento.data === dataFormatada)
                .sort((a, b) => a.horario.localeCompare(b.horario));

            dataAtualSpan.textContent = formatarData(dataSelecionada);
            agendaDiv.style.display = "block"; // Exibe a agenda assim que uma data for selecionada

            if (agendamentosFiltrados.length > 0) {
                for (const agendamento of agendamentosFiltrados) {
                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>${agendamento.horario}</td>
                        <td>${agendamento.paciente} (${agendamento.tutor})</td>
                        <td>${agendamento.status}</td>
                        <td>
                            <button class="editar" onclick="editarAgendamento(${agendamento.id_agendamento})">Editar</button>
                        </td>
                    `;
                    listaAgendamentos.appendChild(row);
                }
            } else {
                // Se não houver agendamentos, exibe a mensagem padrão e mantém a tabela visível
                listaAgendamentos.innerHTML = `<tr><td colspan="4" style="text-align:center;">Nenhum agendamento encontrado para este dia.</td></tr>`;
            }
        } catch (error) {
            console.error("Erro ao carregar agendamentos:", error);
            listaAgendamentos.innerHTML = `<tr><td colspan="4" style="text-align:center; color: red;">Erro ao carregar agendamentos.</td></tr>`;
            agendaDiv.style.display = "block"; // Garante que a agenda seja exibida mesmo se houver erro
        }
    }

    // Atualiza os agendamentos ao escolher uma data
    dataInput.addEventListener("change", function () {
        carregarAgendamentos(this.value);
    });

    // Carrega os agendamentos ao abrir a página
    if (dataInput.value) {
        carregarAgendamentos(dataInput.value);
    }
});

document.getElementById("cadastroForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const id = document.getElementById("id_agendamento").value;
    const status = document.getElementById("status").value;
    const horario = document.getElementById("horario").value;

    if (!id || !status || !horario) {
        alert("Todos os campos são obrigatórios!");
        return;
    }

    try {
        const response = await fetch(`/api/agendamentos/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ horario, status }),
        });

        const data = await response.json();

        if (response.ok) {
            alert("Agendamento atualizado com sucesso!");
            fecharPopupEdicao();
            carregarAgendamentos(document.getElementById("dataSelecionada").value);
        } else {
            alert(`Erro: ${data.erro}`);
        }
    } catch (error) {
        console.error("Erro ao atualizar agendamento:", error);
    }
});

async function carregarStatus() {
    try {
        const response = await fetch("/api/status");
        const statusData = await response.json();

        let statusSelect = document.getElementById("status");
        if (!statusSelect) {
            console.error("Elemento select de status não encontrado!");
            return;
        }

        statusSelect.innerHTML = '<option value="">Selecione</option>';

        statusData.forEach(status => {
            let option = document.createElement("option");
            option.value = status.id;
            option.textContent = status.nome;
            statusSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Erro ao carregar status:", error);
    }
}

async function editarAgendamento(id) {
    try {
        // Buscar os dados do agendamento selecionado
        const response = await fetch(`/api/agendamentos/${id}`);
        const agendamento = await response.json();

        if (!agendamento || agendamento.erro) {
            console.error("Agendamento não encontrado!");
            return;
        }

        // Carregar a página de edição no popup
        const htmlResponse = await fetch("/editar_agendamento");
        document.getElementById("popupContainer").innerHTML = await htmlResponse.text();

        // Garantir que os elementos do popup foram carregados antes de preenchê-los
        await carregarStatus();

        document.getElementById("id_agendamento").value = agendamento.id_agendamento;
        document.getElementById("data").value = formatarData(agendamento.data);
        document.getElementById("tutor").value = agendamento.tutor;
        document.getElementById("paciente").value = agendamento.paciente;
        document.getElementById("horario").value = agendamento.horario;
        document.getElementById("status").value = agendamento.id_status;

        // Exibir o popup
        document.getElementById("editar-popup").style.display = "flex";
    } catch (error) {
        console.error("Erro ao abrir popup de edição:", error);
    }
}


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

function abrirPopupCadastro(dataSelecionada) {
    fetch("/cadastro_agendamento_page")
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
    if (!data) return "";
    return data.split("-").reverse().join("/");
}



window.abrirPopupCadastro = abrirPopupCadastro;
window.fecharPopupCadastro = fecharPopupCadastro;
window.editarAgendamento = editarAgendamento;
window.fecharPopupEdicao = fecharPopupEdicao;