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

function editarTutor(id) {
    fetch("/api/tutores")
        .then(response => response.json())
        .then(tutores => {
            let tutor = tutores.find(p => p.id === parseInt(id));
            if (!tutor) {
                console.error("Tutor não encontrado!");
                return;
            }

            // Preencher os campos do formulário no popup
            document.getElementById("nome").value = tutor.nome;
            document.getElementById("nascimento").value = formatarData(tutor.nascimento);
            document.getElementById("cpf").value = tutor.cpf;
            document.getElementById("telefone").value = tutor.telefone;
            document.getElementById("endereco").value = tutor.endereco;

            // Exibir o popup
            document.getElementById("cadastro-popup").style.display = "block";
        })
            .catch(error => console.error("Erro ao buscar tutor:", error));
}


function formatarData(data) {
    let partes = data.split("-");
    return `${partes[2]}-${partes[1]}-${partes[0]}`; // Invertendo para formato esperado no input
}

window.fecharPopupCadastro = fecharPopupCadastro;
window.editarTutor = editarTutor; // Adiciona a função ao escopo global