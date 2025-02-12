document.addEventListener("DOMContentLoaded", carregarUsuarios);

document.getElementById("novoCadastro").addEventListener("click", function () {
    fetch("/cadastro_usuario_page")
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

document.getElementById("cadastroForm").addEventListener("submit", function (event) {
    if (event.target.id === "cadastroForm") {
        event.preventDefault();
        const id = event.target.dataset.usuarioId;

        if (id) {
            console.log("Chamando salvarEdicaoUsuario com ID:", id);
            salvarEdicaoUsuario(id);
        } else {
            console.error("ID do usuário não encontrado!");
        }
    }
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
    const formData = new FormData(document.getElementById("cadastroForm"));

    const dados = {
        nome: formData.get("nome")?.trim() || "",
        email: formData.get("email")?.trim() || "",
        senha: formData.get("senha")?.trim() || "",
        cargo: formData.get("cargo") || "",
    };

    // Adiciona a especialidade se o cargo for "vet"
    if (dados.cargo === "vet") {
        dados.especialidade = formData.get("especialidade") || "";
    }

    // Validação: Todos os campos devem estar preenchidos
    if (!dados.nome || !dados.email || !dados.senha || !dados.cargo) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    if (dados.cargo === "vet" && !dados.especialidade) {
        alert("Por favor, preencha a especialidade.");
        return;
    }

    console.log("Enviando dados para o servidor:", JSON.stringify(dados));

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
        .then(data => {
            alert(data.mensagem || "Usuário cadastrado com sucesso!");
            fecharPopupCadastro();
            carregarUsuarios();
        })
        .catch(error => {
        console.error("Erro ao cadastrar tutor:", error);
        alert(error.message)
    });
}

function salvarEdicaoUsuario(id) {
    const cargo = document.getElementById("cargo").value;
    const especialidadeInput = document.getElementById("especialidade");

    const usuarioAtualizado = {
        nome: document.getElementById("nome").value,
        email: document.getElementById("email").value,
        senha: document.getElementById("senha").value,
        cargo: cargo,
        especialidade: cargo === "vet" && especialidadeInput ? especialidadeInput.value : null
    };

    console.log("Enviando dados para atualização:", JSON.stringify(usuarioAtualizado));

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
        .then(data => { // ✅ Agora 'data' está definido corretamente
            console.log("Resposta do servidor:", data);
            alert(data.mensagem || "Usuário atualizado com sucesso!");
            fecharPopupCadastro();
            carregarUsuarios();
        })
        .catch(error => console.error("Erro ao atualizar usuário:", error));
}

function editarUsuario(id) {
    fetch("/cadastro_usuario_page")
        .then(response => response.text())
        .then(html => {
            document.getElementById("popupContainer").innerHTML = html;
            document.getElementById("cadastro-popup").style.display = "flex";

            const form = document.getElementById("cadastroForm");
            if (form) {
                form.dataset.usuarioId = id;
                console.log("ID do usuário definido no dataset:", form.dataset.usuarioId);

                form.addEventListener("submit", function (event) {
                    event.preventDefault();
                    salvarEdicaoUsuario(id);
                });
            } else {
                console.error("Erro: Formulário não encontrado!");
            }

            fetch("/api/usuarios")
                .then(response => response.json())
                .then(usuarios => {
                    let usuario = usuarios.find(u => u.id === parseInt(id));
                    if (!usuario) {
                        console.error("Usuário não encontrado!");
                        return;
                    }

                    document.getElementById("nome").value = usuario.nome;
                    document.getElementById("email").value = usuario.email;
                    document.getElementById("senha").value = usuario.senha;
                    document.getElementById("cargo").value = usuario.cargo;

                    document.getElementById("cargo").addEventListener("change", toggleEspecialidade);

                    if (usuario.cargo === "vet") {
                        let especialidadeSelect = document.getElementById("especialidade");

                        especialidadeSelect.dataset.valor = usuario.especialidade;

                        carregarEspecialidades().then(() => {
                            especialidadeSelect.value = usuario.especialidade;
                        });
                    }

                    toggleEspecialidade();
                })
                .catch(error => console.error("Erro ao buscar usuários:", error));
        })
        .catch(error => console.error("Erro ao carregar popup: ", error));
}

function toggleEspecialidade() {
    let cargo = document.getElementById("cargo").value;
    let especialidadeContainer = document.getElementById("especialidade-container");
    let especialidadeSelect = document.getElementById("especialidade");

    if (cargo === "vet") {
        especialidadeContainer.style.display = "block";
        // Carrega as especialidades apenas se ainda não estiverem carregadas
        if (especialidadeSelect.options.length <= 1) {
            especialidadeSelect.setAttribute("required", "true"); // Adiciona required
            carregarEspecialidades().then(() => {
                let usuarioEspecialidade = especialidadeSelect.dataset.valor;
                if (usuarioEspecialidade) {
                    especialidadeSelect.value = usuarioEspecialidade
                }
            });
        }
    } else {
        especialidadeContainer.style.display = "none";
        especialidadeSelect.removeAttribute("required"); // Remove required se não for "vet"
        especialidadeSelect.value = ""; // Reseta o valor
    }
}

function carregarEspecialidades() {
    return fetch("/api/especialidades")
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

            return especialidadeSelect; // Retorna o select para usar depois
        })
        .catch(error => console.error("Erro ao carregar especialidades:", error));
}

function fecharPopupCadastro() {
    document.getElementById("cadastro-popup").style.display = "none";
}


window.fecharPopupCadastro = fecharPopupCadastro;
window.toggleEspecialidade = toggleEspecialidade;
window.editarUsuario = editarUsuario;
