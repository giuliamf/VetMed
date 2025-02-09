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

function toggleEspecialidade() {
    var cargo = document.getElementById("cargo").value;
    var especialidadeContainer = document.getElementById("especialidade-container");

    if (cargo === "vet") {
        especialidadeContainer.style.display = "block";
    } else {
        especialidadeContainer.style.display = "none";
    }
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
                })
            .catch(error => console.error("Erro ao carregar popup: ", error));
        })
     .catch(error => console.error("Erro ao buscar usuários:", error));
}

function fecharPopupCadastro() {
    document.getElementById("cadastro-popup").style.display = "none";
}


window.fecharPopupCadastro = fecharPopupCadastro;
window.toggleEspecialidade = toggleEspecialidade;
window.editarUsuario = editarUsuario;
