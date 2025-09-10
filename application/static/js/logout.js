function abrirPopupLogout() {
    document.getElementById("logout-popup").style.display = "block";
}

function fecharPopupLogout() {
    document.getElementById("logout-popup").style.display = "none";
}

function logout() {
    fecharPopupLogout();
    window.location.href = "/sair";
}

window.fecharPopupLogout = fecharPopupLogout;
window.logout = logout;
window.abrirPopupLogout = abrirPopupLogout;