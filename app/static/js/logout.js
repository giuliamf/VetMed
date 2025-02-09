document.addEventListener("DOMContentLoaded", function() {
    fetch("../../templates/logout.html") // Caminho do log out.html
        .then(response => response.text())
        .then(data => {
            document.getElementById("popup-container").innerHTML = data;
        })
        .catch(error => console.error("Erro ao carregar popup de logout:", error));
});


function abrirPopupLogout() {
    document.getElementById("popup").style.display = "block";
}

function fecharPopup() {
    document.getElementById("popup").style.display = "none";
}

function logout() {
    fecharPopup();
    window.location.href = "/sair";
}
