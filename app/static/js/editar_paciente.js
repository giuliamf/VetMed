import { getTutor } from './buscas.js';

document.addEventListener("DOMContentLoaded", function () {
    carregarPacientes();
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
function editarPaciente(id) {
    fetch("/api/pacientes")
        .then(response => response.json())
        .then(pacientes => {
            let paciente = pacientes.find(p => p.id === id);
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
