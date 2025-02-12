document.addEventListener("DOMContentLoaded", carregarTutores);

document.getElementById("novoCadastro").addEventListener("click", function () {
    fetch("/cadastro_tutor_page")
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

function carregarTutores() {
    fetch("/api/tutores")
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao buscar tutores");
            }
            return response.json();
        })
        .then(tutores => {
            let tabela = document.getElementById("tabelaTutores");
            tabela.innerHTML = ""; // Limpa a tabela antes de recarregar os dados

            tutores.forEach(tutor => {
                let linha = document.createElement("tr");
                linha.innerHTML = `
                    <td>${tutor.nome} (${tutor.cpf})</td>
                    <td><button onclick="editarTutor('${tutor.id}')">Editar</button></td>
                `;
                tabela.appendChild(linha);
            });
        })
        .catch(error => console.error("Erro ao carregar tutores:", error));
}

function enviarFormulario() {
    const form = document.getElementById("cadastroForm");
    const formData = new FormData(form);

    const dados = {
        nome: formData.get("nome")?.trim() || "",
        cpf: formData.get("cpf")?.trim() || "",
        nascimento: formData.get("nascimento") || "",
        telefone: formData.get("telefone")?.trim() || "",
        endereco: formData.get("endereco")?.trim() || "",
    };

    // Validação: Todos os campos devem estar preenchidos
    if (!dados.nome || !dados.cpf || !dados.nascimento || !dados.telefone || !dados.endereco) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    fetch("/cadastro_tutor", {
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
        alert(response.mensagem || "Tutor cadastrado com sucesso!");
        fecharPopupCadastro();
        carregarTutores(); // Recarregar a lista de tutores
    })
    .catch(error => {
        console.error("Erro ao cadastrar tutor:", error);
        alert(error.message)
    });
}

function salvarEdicaoTutor(id) {
    const tutorAtualizado = {
        cpf: document.getElementById("cpf").value,
        nome: document.getElementById("nome").value,
        nascimento: document.getElementById("nascimento").value,
        telefone: document.getElementById("telefone").value,
        endereco: document.getElementById("endereco").value
    };

    fetch(`/api/tutores/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(tutorAtualizado)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao atualizar tutor");
        }
        return response.json();
    })
    .then(data => {
        alert(data.mensagem);
        fecharPopupCadastro();
        carregarTutores(); // Atualiza a tabela após edição
    })
    .catch(error => console.error("Erro ao atualizar tutor:", error));
}


function editarTutor(id) {
    fetch(`/api/tutores/${id}`)
        .then(response => response.json())
        .then(tutor => {
            if (!tutor) {
                console.error("Tutor não encontrado!");
                return;
            }

            // Preenche os campos com os dados do tutor
            document.getElementById("nome").value = tutor.nome;
            document.getElementById("nascimento").value = formatarData(tutor.nascimento);
            document.getElementById("cpf").value = tutor.cpf;
            document.getElementById("telefone").value = tutor.telefone;
            document.getElementById("endereco").value = tutor.endereco;

            // Atualiza o botão "Salvar" para chamar a função corretamente com o ID
            document.getElementById("cadastroForm").dataset.tutorId = id;

            // Exibe o formulário de edição
            document.getElementById("cadastro-popup").style.display = "block";
        })
        .catch(error => console.error("Erro ao buscar tutor:", error));
}


document.getElementById("cadastroForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Impede o recarregamento da página

    const id = this.dataset.tutorId; // Recupera o ID armazenado
    salvarEdicaoTutor(id);
});

function formatarData(dataCompleta) {
    let data = new Date(dataCompleta); // Converte para objeto Date
    return data.toISOString().split("T")[0]; // Extrai apenas yyyy-MM-dd
}


function fecharPopupCadastro() {
    document.getElementById("cadastro-popup").style.display = "none";
}
