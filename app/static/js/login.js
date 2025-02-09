document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector(".login-form");
    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const senha = document.getElementById("senha").value;
        const errorBox = document.getElementById("error-box");

        const response = await fetch("/", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ email, senha })
        });

        if (!response.ok) {
            const data = await response.json();
            errorBox.innerText = data.erro;
            errorBox.style.display = "block";
        } else {
            window.location.href = "/inicio"; // Redireciona se o login for bem-sucedido
        }
    });
});