document.addEventListener("DOMContentLoaded", carregarPacientes);

document.getElementById("novoCadastro").addEventListener("click", function () {
    fetch("/cadastro_paciente_page")
        .then(response => response.text())
        .then(html => {
            document.getElementById("popupContainer").innerHTML = html;
            document.getElementById("cadastro-popup").style.display = "flex";

            document.getElementById("cadastroForm").addEventListener("submit", function (event) {
                event.preventDefault();
                enviarFormulario();
            });
        })
        .catch(error => console.error("Erro ao carregar popup: ", error));
});

function carregarPacientes() {
    fetch("/api/pacientes")
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao buscar pacientes");
            }
            return response.json();
        })
        .then(pacientes => {
            let tabela = document.getElementById("tabelaPacientes");
            tabela.innerHTML = ""; // Limpa a tabela antes de recarregar os dados

            pacientes.forEach(paciente => {
                let linha = document.createElement("tr");
                linha.innerHTML = `
                    <td>${paciente.nome} (${paciente.nome_tutor})</td>
                    <td>
                        <button onclick="editarPaciente('${paciente.id_animal}')">Editar</button>
                        <button onclick="excluirPaciente(${paciente.id_animal})">Excluir</button>
                    </td>
                `;
                tabela.appendChild(linha);
            });
        })
        .catch(error => console.error("Erro ao carregar pacientes:", error));
}

function enviarFormulario() {
    const form = document.getElementById("cadastroForm");
    const formData = new FormData(form);

    const dados = {
        nome: formData.get("nome")?.trim() || "",
        nascimento: formData.get("nascimento") || "",
        especie: formData.get("especie")?.trim() || "",
        raca: formData.get("raca")?.trim() || "",
        peso: formData.get("peso")?.trim() || "",
        cor: formData.get("cor")?.trim() || "",
        sexo: formData.get("sexo") || "",
        tutor: formData.get("tutor")?.trim() || "",
    }

    // Validação: Todos os campos devem estar preenchidos
    if (!dados.nome || !dados.nascimento || !dados.especie || !dados.raca || !dados.peso || !dados.cor || !dados.sexo || !dados.tutor) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    fetch("/cadastro_paciente", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dados)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(error => { throw new Error(error.erro || "Erro desconhecido"); });
        }
        return response.json();
    })
    .then(response => {
        alert(response.mensagem || "Paciente cadastrado com sucesso!");
        fecharPopupCadastro()
        carregarPacientes()
    })
        .catch(error => {
            console.error("Erro ao cadastrar paciente:", error);
            alert(error.message);
        })
}

function salvarEdicaoPaciente(id){
    const pacienteAtualizado = {
        nome: document.getElementById("nome").value,
        nascimento: document.getElementById("nascimento").value,
        especie: document.getElementById("especie").value,
        raca: document.getElementById("raca").value,
        peso: document.getElementById("peso").value,
        cor: document.getElementById("cor").value,
        sexo: document.getElementById("macho").checked ? "M" : "F",
        tutor: document.getElementById("tutor").value
    };

    fetch(`/api/pacientes/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(pacienteAtualizado)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao atualizar paciente 2");
        }
        return response.json();
    })
    .then(data => {
        alert(data.mensagem);
        fecharPopupCadastro();
        carregarPacientes(); // Atualiza a tabela após edição
    })
    .catch(error => console.error("Erro ao atualizar paciente 3:", error)
    );
}

// Função para preencher os dados no popup de edição
function editarPaciente(id) {
    fetch(`/api/pacientes/${id}`)
        .then(response => response.json())
        .then(paciente => {
            if (!paciente) {
                console.error("Paciente não encontrado!");
                return;
            }

            // Preencher os campos do formulário no popup
            document.getElementById("nome").value = paciente.nome;
            document.getElementById("nascimento").value = formatarData(paciente.nascimento);
            document.getElementById("especie").value = paciente.especie;
            document.getElementById("raca").value = paciente.raca;
            document.getElementById("peso").value = paciente.peso;
            document.getElementById("cor").value = paciente.cor;
            document.getElementById("tutor").value = paciente.tutor;

            document.getElementById("tutor").setAttribute("disabled", "true");

            // Definir sexo
            if (paciente.sexo === "M") {
                document.getElementById("macho").checked = true;
            } else if (paciente.sexo === "F") {
                document.getElementById("femea").checked = true;
            }

            // Atualiza o botão "Salvar" para chamar a função corretamente com o ID
            document.getElementById("cadastroForm").dataset.pacienteId = id;

            // Exibir o popup
            document.getElementById("cadastro-popup").style.display = "block";
        })
        .catch(error => console.error("Erro ao buscar paciente:", error));
}

document.getElementById("cadastroForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const id = this.dataset.pacienteId;
    salvarEdicaoPaciente(id);
});

function fecharPopupCadastro() {
    document.getElementById("cadastro-popup").style.display = "none";
}

function formatarData(dataCompleta) {
    let data = new Date(dataCompleta); // Converte para objeto Date
    return data.toISOString().split("T")[0]; // Extrai apenas yyyy-MM-dd
}

function excluirPaciente(id) {
    if (!confirm("Tem certeza que deseja excluir este paciente?")) {
        return;
    }

    fetch(`/api/pacientes/${id}`, {
        method: "DELETE"
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao excluir paciente");
        }
        return response.json();
    })
    .then(data => {
        alert(data.mensagem);
        carregarPacientes();
    })
    .catch(error => console.error("Erro ao excluir paciente:", error));
}

window.fecharPopupCadastro = fecharPopupCadastro;
window.editarPaciente = editarPaciente;
window.excluirPaciente = excluirPaciente;