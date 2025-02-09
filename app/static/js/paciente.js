import { getTutor, buscarTutorCpf } from './buscas.js';

document.getElementById("novoCadastro").addEventListener("click", function () {
    fetch("/cadastro_paciente")
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

// Função para carregar os pacientes da API e atualizar a tabela (caso precise no futuro)
function carregarPacientes() {
    fetch("/api/pacientes")
        .then(response => response.json())
        .then(pacientes => {
            pacientes.forEach(paciente => {
                let botaoEditar = document.querySelector(`button[onclick="editarPaciente('${paciente.id}')"]`);
                if (botaoEditar) {
                    botaoEditar.addEventListener("click", () => editarPaciente(paciente.id));
                }
            });
        })
        .catch(error => console.error("Erro ao carregar pacientes:", error));
}

// Função para preencher os dados no popup de edição
export function editarPaciente(id) {
    fetch("/api/pacientes")
        .then(response => response.json())
        .then(pacientes => {
            let paciente = pacientes.find(p => p.id === parseInt(id));
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

            // Pegar o objeto do tutor
            getTutor(paciente.tutor)
                .then(tutor => {
                    if (tutor) {
                        document.getElementById("tutor").value = tutor.cpf;
                    }
                })
                .catch(error => console.error("Erro ao buscar tutor: ", error));

            // Definir sexo
            if (paciente.sexo === "M") {
                document.getElementById("macho").checked = true;
            } else if (paciente.sexo === "F") {
                document.getElementById("femea").checked = true;
            }

            // Exibir o popup
            document.getElementById("cadastro-popup").style.display = "block";
        })
        .catch(error => console.error("Erro ao buscar paciente:", error));
}

// Função para enviar o formulário de edição
function enviarEdicao() {

}

// Formatar a data para YYYY-MM-DD (necessário para o input date)
function formatarData(data) {
    let partes = data.split("-");
    return `${partes[2]}-${partes[1]}-${partes[0]}`; // Invertendo para formato esperado no input
}

function enviarFormulario() {
    const form = document.getElementById("cadastroForm");
    const formData = new FormData(form);

    // Achar tutor pelo CPF
    const cpf = formData.get("tutor");
    buscarTutorCpf(cpf).then(tutor => {
        if (!tutor) {
            alert("Tutor não encontrado! Cadastre o tutor antes de cadastrar o paciente.");
            return;
        }

        // Enviar dados do formulário
        const data = {
            nome: formData.get("nome"),
            tutor: tutor.id,
            especie: formData.get("especie"),
            raca: formData.get("raca"),
            nascimento: formData.get("nascimento"),
            sexo: formData.get("sexo"),
            peso: parseFloat(formData.get("peso")),
            cor: formData.get("cor")
        };

        fetch("/cadastro_paciente", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(response => {
                if (response.status === "success") {
                    alert("Paciente cadastrado com sucesso!");
                    fecharPopupCadastro();
                } else {
                    alert("Erro ao cadastrar paciente: " + response.message);
                }
            })
            .catch(error => console.error("Erro ao cadastrar paciente: ", error));

        });
}

function fecharPopupCadastro() {
    console.log("Fechando popup de cadastro");
    document.getElementById("cadastro-popup").style.display = "none";
}

window.fecharPopupCadastro = fecharPopupCadastro;
window.editarPaciente = editarPaciente;