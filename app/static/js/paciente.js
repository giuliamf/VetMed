document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("cadastroFormPaciente").addEventListener("submit", validarTutorCPF);
    carregarPacientes();
});

document.getElementById("novoCadastro").addEventListener("click", function () {
    fetch("/cadastro_paciente")  // Faz a requisição AJAX para pegar a popup
        .then(response => response.text())
        .then(html => {
            document.getElementById("popupContainer").innerHTML = html;
            document.getElementById("cadastro-popup").style.display = "flex";

            // Adiciona o evento de envio ao formulário (validação do CPF)
            document.getElementById("cadastroForm").addEventListener("submit", validarTutorCPF);
        })
        .catch(error => console.error("Erro ao carregar popup: ", error));
});

function validarTutorCPF(event) {
    event.preventDefault(); // Impede o envio do formulário até a validação

    let cpfInput = document.getElementById("tutor");
    let cpf = cpfInput.value.replace(/\D/g, ""); // Remove caracteres não numéricos
    let mensagem = document.getElementById("tutor-verificacao");

    if (cpf.length !== 11) {
        mensagem.style.display = "inline";
        mensagem.innerText = "CPF inválido!";
        return;
    }

    cpfInput.value = cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4"); // Formata CPF

    // Verifica no banco se o CPF existe
    fetch(`/api/verificar_tutor/${cpf}`)
        .then(response => response.json())
        .then(data => {
            if (data.existe) {
                mensagem.style.display = "none"; // Esconde mensagem de erro
                document.getElementById("cadastroForm").submit(); // Envia o formulário
            } else {
                mensagem.style.display = "inline";
                mensagem.innerText = "Tutor não encontrado!";
            }
        })
        .catch(error => {
            console.error("Erro ao verificar CPF:", error);
            mensagem.style.display = "inline";
            mensagem.innerText = "Erro ao verificar CPF!";
        });
}


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
                    <td>${paciente.nome} (<span>${paciente.cpf_tutor}</span>)</td>
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
            document.getElementById("nascimento").value = formatarData(paciente.ano_nascimento);
            document.getElementById("especie").value = paciente.especie;
            document.getElementById("raca").value = paciente.raca;
            document.getElementById("peso").value = paciente.peso;
            document.getElementById("cor").value = paciente.cor;
            document.getElementById("tutor").value = paciente.cpf_tutor; // Agora mostra o CPF correto

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
    if (!data) return "";

    let partes = data.split("-");
    if (partes.length === 3) {
        return `${partes[0]}-${partes[1]}-${partes[2]}`; // Mantém formato YYYY-MM-DD
    }
    return data; // Retorna a data original caso não seja necessário formatar
}
