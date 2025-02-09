function abrirPopupLogout() {
    document.getElementById("logout-popup").style.display = "block";
}

function fecharPopupLogout() {
    document.getElementById("logout-popup").style.display = "none";
}

function logout() {
    fecharPopup();
    window.location.href = "/sair";
}
