document.addEventListener("DOMContentLoaded", function () {
    carregarPacientes();
});

// Função para carregar os pacientes da API e atualizar a tabela
function carregarPacientes() {
    fetch("/api/pacientes")
        .then(response => response.json())
        .then(pacientes => {
            let tabelaPacientes = document.querySelector("tbody");
            tabelaPacientes.innerHTML = ""; // Limpa a tabela antes de preencher

            pacientes.forEach(paciente => {
                let novaLinha = document.createElement("tr");

                novaLinha.innerHTML = `
                    <td>${paciente.nome} (<span>${paciente.tutor}</span>)</td>
                    <td>
                        <button onclick="editarPaciente('${paciente.id_animal}')">Editar</button>
                    </td>
                `;

                tabelaPacientes.appendChild(novaLinha);
            });
        })
        .catch(error => console.error("Erro ao carregar pacientes:", error));
}

// Função para preencher os dados no popup de edição
export function editarPaciente(id) {
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
            document.getElementById("tutor").value = paciente.cpf_tutor;  // Atualizado para CPF do tutor

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

// Formatar a data para YYYY-MM-DD (necessário para o input date)
function formatarData(data) {
    let partes = data.split("-");
    return `${partes[0]}-${partes[1]}-${partes[2]}`;
}
