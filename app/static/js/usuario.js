document.addEventListener("DOMContentLoaded", carregarUsuarios);

document.getElementById("novoCadastro").addEventListener("click", function () {
    fetch("/cadastro_usuario")
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

function carregarUsuarios() {
    fetch("/api/usuarios")
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao buscar usuários");
            }
            return response.json();
        })
        .then(usuarios => {
            let tabela = document.getElementById("tabelaUsuarios");
            tabela.innerHTML = ""; // Limpa a tabela antes de recarregar os dados

            usuarios.forEach(usuario => {
                let linha = document.createElement("tr");
                linha.innerHTML = `
                    <td>${usuario.nome} - ${usuario.cargo === 'vet' ? 'Veterinário(a)' : usuario.cargo === 'sec' ? 'Secretário(a)' : usuario.cargo}</td>
                    <td><button onclick="editarUsuario('${usuario.id}')">Editar</button></td>
                `;
                tabela.appendChild(linha);
            });
        })
        .catch(error => console.error("Erro ao carregar usuários:", error));
}

function enviarFormulario() {
    const form = document.getElementById("cadastroForm");
    const formData = new FormData(form);

    // Só considera a especialidade, caso ela não seja undefined
    const cargo = formData.get("cargo") || "";
    const especialidade = cargo === "vet" ? formData.get("especialidade")?.trim() || "" : undefined;

    const dados = {
        nome: formData.get("nome")?.trim() || "",
        email: formData.get("email")?.trim() || "",
        senha: formData.get("senha")?.trim() || "",
        cargo: cargo,
        ...(especialidade !== undefined && { especialidade }) // Adiciona a especialidade apenas caso ela exista (vet)
    };

    // Validação: Todos os campos devem estar preenchidos
    if (!dados.nome || !dados.email || !dados.senha || !dados.cargo) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    if (dados.cargo === "vet" && !dados.especialidade) {
        alert("Por favor, preencha a especialidade.");
        return;
    }

    fetch("/cadastro_usuario", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(dados),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao cadastrar usuário");
            }
            return response.json();
        })
        .then(() => {
            alert(response.mensagem || "Tutor cadastrado com sucesso!");
            fecharPopupCadastro();
            carregarUsuarios();
        })
        .catch(error => {
        console.error("Erro ao cadastrar tutor:", error);
        alert(error.message)
    });
}

function salvarEdicaoUsuario(id) {
    const usuarioAtualizado = {
        nome: document.getElementById("nome").value,
        email: document.getElementById("email").value,
        senha: document.getElementById("senha").value,
        cargo: document.getElementById("cargo").value,
        especialidade: document.getElementById("especialidade").value, // caso não seja vet, o valor é vazio
    };

    fetch(`/api/usuarios/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(usuarioAtualizado)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao atualizar usuário");
            }
            return response.json();
        })
        .then(() => {
            alert(data.mensagem);
            fecharPopupCadastro();
            carregarUsuarios();
        })
        .catch(error => console.error("Erro ao atualizar usuário:", error));
}

function editarUsuario(id) {
    fetch("/api/usuarios")
        .then(response => response.json())
        .then(usuarios => {
            let usuario = usuarios.find(u => u.id === parseInt(id));
            if (!usuario) {
                console.error("Usuário não encontrado!")
                return
            }

            fetch("/cadastro_usuario")
                .then(response => response.text())
                .then(html => {
                    document.getElementById("popupContainer").innerHTML = html;
                    document.getElementById("cadastro-popup").style.display = "flex";

                    document.getElementById("nome").value = usuario.nome;
                    document.getElementById("email").value = usuario.email;
                    document.getElementById("senha").value = usuario.senha;
                    document.getElementById("cargo").value = usuario.cargo;

                    toggleEspecialidade()

                    if (usuario.cargo === "vet") {
                        document.getElementById("especialidade").value = usuario.especialidade;
                    } else {
                        document.getElementById("especialidade").value = "";
                    }
                    document.getElementById("cargo").addEventListener("change", toggleEspecialidade);
                    document.getElementById("cadastroForm").dataset.usuarioId = id;
                    document.getElementById("cadastro-popup").style.display = "block";
                })
                .catch(error => console.error("Erro ao carregar popup: ", error));
        })
        .catch(error => console.error("Erro ao buscar usuários:", error));
}

document.getElementById("cadastroForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const id = event.target.dataset.usuarioId;
    salvarEdicaoUsuario(id);
});

function toggleEspecialidade() {
    let cargo = document.getElementById("cargo").value;
    let especialidadeContainer = document.getElementById("especialidade-container");
    let especialidadeSelect = document.getElementById("especialidade");

    if (cargo === "vet") {
        especialidadeContainer.style.display = "block";
        carregarEspecialidades();
    } else {
        especialidadeContainer.style.display = "none";
        especialidadeSelect.innerHTML = '<option value="">Selecione</option>'
    }
}

function carregarEspecialidades() {
    fetch("/api/especialidades")
        .then(response => response.json())
        .then(especialidades => {
            let especialidadeSelect = document.getElementById("especialidade");
            especialidadeSelect.innerHTML = '<option value="">Selecione</option>';

            especialidades.forEach(especialidade => {
                let option = document.createElement("option");
                option.value = especialidade.id;
                option.innerText = especialidade.nome;
                especialidadeSelect.appendChild(option);
            });
        })
        .catch(error => console.error("Erro ao carregar especialidades:", error));
}

function fecharPopupCadastro() {
    document.getElementById("cadastro-popup").style.display = "none";
}


window.fecharPopupCadastro = fecharPopupCadastro;
window.toggleEspecialidade = toggleEspecialidade;
window.editarUsuario = editarUsuario;
