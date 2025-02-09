document.getElementById("novoCadastro").addEventListener("click", function () {
    fetch("/cadastro_tutor")
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

function enviarFormulario() {
}

function fecharPopupCadastro() {
    document.getElementById("cadastro-popup").style.display = "none";
}