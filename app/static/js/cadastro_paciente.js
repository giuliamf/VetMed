import { buscarTutorCpf } from './buscas.js';

document.getElementById("novoCadastro").addEventListener("click", function () {
    fetch("/cadastro_paciente")
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
    const form = document.getElementById("cadastroForm");
    const formData = new FormData(form);

    // Achar tutor pelo CPF
    const cpf = formData.get("tutor");
    buscarTutorCpf(cpf).then(tutor => {
        if (!tutor) {
            alert("Tutor não encontrado! Cadastre o tutor antes de cadastrar o paciente.");
            return;
        }

        // Enviar dados do formulário
        const data = {
            nome: formData.get("nome"),
            tutor: tutor.id,
            especie: formData.get("especie"),
            raca: formData.get("raca"),
            nascimento: formData.get("nascimento"),
            sexo: formData.get("sexo"),
            peso: parseFloat(formData.get("peso")),
            cor: formData.get("cor")
        };

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
                    fecharPopupCadastro();
                } else {
                    alert("Erro ao cadastrar paciente: " + response.message);
                }
            })
            .catch(error => console.error("Erro ao cadastrar paciente: ", error));

        });
}

function fecharPopupCadastro() {
    console.log("Fechando popup de cadastro");
    document.getElementById("cadastro-popup").style.display = "none";
}

window.fecharPopupCadastro = fecharPopupCadastro; // Adiciona a função ao escopo global