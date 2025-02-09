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


function fecharPopupCadastro() {
    document.getElementById("cadastro-popup").style.display = "none";
}


window.fecharPopupCadastro = fecharPopupCadastro;
window.toggleEspecialidade = toggleEspecialidade;
