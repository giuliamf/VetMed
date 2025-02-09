document.getElementById("novoCadastro").addEventListener("click", function () {
    fetch("/cadastro_paciente")
        .then(response => response.text())
        .then(html => {
            document.getElementById("popupContainer").innerHTML = html;
            document.getElementById("popup").style.display = "flex";

            document.getElementById("cadastroForm").addEventListener("submit", function (event) {
                event.preventDefault();
                enviarFormulario();
            });
        })
        .catch(error => console.error("Erro ao carregar popup: ", error));
});

function enviarFormulario() {
    const form = document.getElementById("cadastroForm");
    const formData = new FormData(form);

    const data = {};
    formData.forEach((value, key) => data[key] = value);

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
                fecharPopup();
            } else {
                alert("Erro ao cadastrar paciente: " + response.message);
            }
        })
        .catch(error => console.error("Erro ao cadastrar paciente: ", error));
}

function editarPaciente(nome) {
    alert("Editar paciente: " + nome);
}